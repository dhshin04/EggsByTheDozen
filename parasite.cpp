#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/opencv.hpp"
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

using namespace cv;
using namespace std;

struct Parasite {
    float centerX;
    float centerY; 
    float width;
    float height;
    float estArea;
    Parasite() {};
    Parasite(float cx, float cy, float w, float h, float a) : centerX(cx), centerY(cy), width(w), height(h), estArea(a) {};
};

vector<Parasite> readAnnotations(string name) {
    vector<Parasite> Annotations;
    cout << name;

    ifstream file("../" + name);

    if (!file) {
        std::cerr << "Unable to open file." << std::endl;
    }

    Parasite para;
    while (file >> para.centerX >> para.centerY >> para.width >> para.height) {
        para.estArea = para.width * para.height;
        Annotations.push_back(para);
    }

    file.close();

    for (const auto& r : Annotations) {
        std::cout << "Parasite: "
                  << "CenterX = " << r.centerX << ", "
                  << "CenterY = " << r.centerY << ", "
                  << "Width = " << r.width << ", "
                  << "Height = " << r.height << std::endl;
    }
    return Annotations;
}

float calculateSquaredDistance(float x1, float y1, float x2, float y2) {
    return std::pow(x2 - x1, 2) + std::pow(y2 - y1, 2);
}

vector<int> calculateError(const vector<Parasite>& expected, const vector<Parasite>& observed) {
    int expSize = expected.size(); int obSize = observed.size();
        vector<int> MissNums;

    if (obSize > expSize * 1.5) { 
        cout << "Too many detected parasites, increase binary threshold." << "\n";
        return MissNums;
    }
    else if (obSize < expSize * 0.4) { 
        cout << "Not enough detected parasites, decrease binary threshold." << "\n";
        return MissNums;
    }

    int DUPLICATES = 0;
    int MISSES = 0;
    float totalError = 0;
    int UNDETECTED = 0;

    vector<int> detectionPaired(obSize, 1); 

    Parasite p1; Parasite p2;
    for (int i=0; i<expSize; i++) {
        float maxDist = 901;
        float currDist = 0;
        bool paired = false;
        p1 = expected[i];
        for (int a=0; a<obSize; a++) {
            p2 = observed[a];
            currDist = calculateSquaredDistance(p1.centerX, p1.centerY, p2.centerX, p2.centerY);
            if (currDist < 900) { 
                detectionPaired[a] = 0;
                float realDist = sqrt(currDist);

                if (!paired) {
                    paired = true;
                    totalError += 0.1 * realDist;
                }
                else {
                    DUPLICATES ++;
                    cout << "DUPLICATE parasite detection found at " << p2.centerX << "," << p2.centerY << "\n";
                    totalError += 0.5 * realDist;
                }
                cout << "\n" << "OBSERVED PARASITE found at " << p2.centerX << "," << p2.centerY << "\n";
                cout << realDist << " from expected parasite at " << p1.centerX << ", " << p1.centerY << "\n";

                if (currDist < maxDist) {
                    maxDist = currDist; 
                }
            }
        }
        if (maxDist == 901) {
            cout << "Undetected Barber Worm Egg!!! at " << p1.centerX << "," <<  p1.centerY << "\n";
            UNDETECTED ++;
        }
    }
    for (int i=0; i<detectionPaired.size(); i++) {
        int num = detectionPaired[i];
        if (num ==1) { MissNums.push_back(i); }
        MISSES += num;
    }
    cout << "\n-----------PERFORMANCE-----------\n" << "\nParasites Expected: " << expSize << "\n";
    cout << "\nParasites Detected: " << obSize << "\n";
    cout << "\nUndetected Parasite Eggs: " << UNDETECTED << "\n";
    cout << "\nFalse Positive Eggs: " << MISSES << "\n\n";
    cout << "\n---------ERROR ANALYSIS----------\n";
    cout << "\nDistanceError: " << totalError << "\n";
    totalError += 5*MISSES;
    totalError += 20*UNDETECTED;
    cout << "\nTotal Error Score: " << totalError;
    cout << "\n\n";
    
    return MissNums;
}

int main(int argc, const char* argv[]) {

    
    Mat gray;
    Mat image;
    Mat_<Vec3d> im;
    bool saveImages = true;
    bool displayImage = true;
    int ht = 230; //higher threshold value
    int ct = 30; //center threshold, votes
    int minRad = 5; //minimum considered detection
    int maxRad = 20;
    int mdd = 30; //min distance denominator: what the min distance between centers is divided into (larger value = smaller mindist)
    string fileName = "";
    vector<Parasite> Annotations;

    for(int i =0; i<argc; i++){ 
        if(strcmp(argv[i], "-f") == 0){
            fileName = argv[i+1];
            image = imread(argv[i+1],1);
            im =imread(argv[i+1],1);
            gray = imread(argv[i+1],IMREAD_GRAYSCALE); //grayscale input image
            cout << "file processed\n";
        }
        if(strcmp(argv[i], "-ht") == 0){ //cannyedge thresh
            ht = stoi(argv[i+1]);
        }
        if(strcmp(argv[i], "-ct") == 0){ //center voting thresh
            ct = stoi(argv[i+1]);
        }
        if(strcmp(argv[i], "-minr") == 0){ //minimum radius detected by hough circles
            minRad = stoi(argv[i+1]);
        }
        if(strcmp(argv[i], "-maxr") == 0){ //maximum radius 
            maxRad = stoi(argv[i+1]);
        }
        if(strcmp(argv[i], "-mdd") == 0){
            mdd = stoi(argv[i+1]);
        }
        if (strcmp(argv[i], "-save") == 0) {
            int saveVal = stoi(argv[i+1]);
            saveImages = (saveVal==1) ? true : false;
        }
        if (strcmp(argv[i], "-display") == 0) {
            int dispVal = stoi(argv[i+1]);
            displayImage = (dispVal==1) ? true : false;
        }
    }
    try {
        Annotations = readAnnotations(fileName + ".txt");
    }
    catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    int imgArea = image.cols * image.rows;

    cout << "Image Width: " << image.cols << "\n";
    cout << "Image Height: " << image.rows << "\n";
    cout << "Image Area: " << imgArea << "\n";

    cvtColor(image, gray, COLOR_BGR2GRAY, 0);
    if (saveImages) imwrite("imageg.png", gray);

    Mat edges; Mat cannyout;
    medianBlur(gray, gray, 5);
    GaussianBlur(gray, gray, Size(3, 3), 0, 0, BORDER_DEFAULT);

    Mat thresh; 
    threshold(gray, thresh, ht, 255, THRESH_BINARY);
    if (saveImages) {
        imwrite("imaget.png", thresh);
    }


    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
    findContours(thresh, contours, hierarchy, RETR_TREE, CHAIN_APPROX_NONE);

    // ----- TEST CONTOURS ---- //

     Mat contourMap = image.clone();
    
    drawContours(contourMap, contours, -1, Scalar(0,0,100),2);

    if (displayImage) {
        imshow("Debri Contours", contourMap);
        waitKey(0);
    }


    // ----------------------- //
    vector<Parasite> detectedParasites;


    for (size_t i = 0; i < contours.size(); i++) {
        // Calculate contour area and bounding rectangle
        double area = static_cast<int>(cv::contourArea(contours[i]));
        cv::Rect boundingBox = cv::boundingRect(contours[i]);
        double aspectRatio = (double)boundingBox.width / boundingBox.height;

        // Filter based on aspect ratio and minimum size
        double elongationFactor = std::abs(1-aspectRatio);

        if (elongationFactor > 0.1 && elongationFactor<1 && area > 1000 && area < 4000) {
            // Approximate contour to smooth shape
            std::vector<cv::Point> approx;  
            cv::approxPolyDP(contours[i], approx, 0.01 * cv::arcLength(contours[i], true), true);
            
            

            if (approx.size() > 4) { // Need at least 5 points to fit ellipse
                cv::RotatedRect fittedEllipse = cv::fitEllipse(approx);

                // Further checks can be added here, e.g., comparing the area of the contour to the area of the fitted ellipse

                // Draw the ellipse

                cv::ellipse(image, fittedEllipse, cv::Scalar(255, 0, 0), 2);
                
                cv::Point2f centerPoint = fittedEllipse.center;
                cv::Point point(static_cast<int>(centerPoint.x), static_cast<int>(centerPoint.y));
                cv::circle(image, point, 2, cv::Scalar(0,0,255), -1);

                Parasite p(centerPoint.x, centerPoint.y, boundingBox.width, boundingBox.height, boundingBox.width*boundingBox.height);
                detectedParasites.push_back(p);

                std::string text = "(" + std::to_string(point.x) + ", " + std::to_string(point.y) + ")";
                int fontFace = cv::FONT_HERSHEY_SIMPLEX;
                double fontScale = 0.5;
                int textThickness = 1;
                cv::Point textOrg(point.x + 10, point.y - 10); // Position the text slightly right and above the point
                cv::Scalar textColor(0, 0, 0); // White color for the text

                // Put the text on the image
                cv::putText(image, text, textOrg, fontFace, fontScale, textColor, textThickness);

                cout << "Location: " << point << "\tArea" << area << "\n";
            }
        }
    }

    // CALCULATE ERROR //
    vector<int> missed_guesses = calculateError(Annotations, detectedParasites);
    for (int guess : missed_guesses) {
        Point center(detectedParasites[guess].centerX,detectedParasites[guess].centerY);
        int size = 50;

        // Define the color of the "X" (red in BGR format)
        cv::Scalar color(0, 0, 255);  // Red color

        // Draw two lines to form the "X"
        // Line from top-left to bottom-right
        cv::line(image, cv::Point(center.x - size / 2, center.y - size / 2),
                cv::Point(center.x + size / 2, center.y + size / 2), color, 2);

        // Line from bottom-left to top-right
        cv::line(image, cv::Point(center.x - size / 2, center.y + size / 2),
                cv::Point(center.x + size / 2, center.y - size / 2), color, 2);
    }


    if (displayImage) {
        Mat image_copy = image.clone();
        imshow("None approximation", image_copy);
        waitKey(0);
        imwrite("output.jpg", image_copy);
        destroyAllWindows();
    }
    


    //Canny(gray, cannyout, ht/1.4, ht, 3); //grayscale image, edges out, low thresh, high thresh, sobel kernel (3x3)
    //edges = Scalar::all(0);
    //gray.copyTo(edges, cannyout);
    //imwrite("./imagef.jpg", edges);

    
    /*vector<Vec3f> circles;
    HoughCircles(gray, circles, HOUGH_GRADIENT, 1, //grayscale image, vector w xyrad for circles, gradient, inverse resolution ratio, min distance between centers, threshold for cannyedge, threshold for centers, minrad, maxrad;
                 gray.rows/mdd,  
                 ht, ct, minRad, maxRad);

    int maxdetectrad = 0;
    for( size_t i = 0; i < circles.size(); i++ ) //display centers and outlines
    {
        Vec3i c = circles[i];
        Point center = Point(c[0], c[1]); // c = h, k, rad
        // circle center: #circle(image, center, 1, Scalar(0,100,100), 3, LINE_AA);
        int radius = c[2];
        if(radius>maxdetectrad){
            maxdetectrad = radius;
        }
        //pennies red, quarters purple, nickel yellow
        circle(image, center, radius, Scalar(0,0,255), 4, LINE_AA); //detected circles in red, thickness = 4 TEMPORARILY BLACK
    }
    imwrite("./imageCircles.jpg",image);*/

}
/*
    Mat gray;
    Mat image;
    Mat_<Vec3d> im;
    int ht = 100; //higher threshold value for canny edge, lower is twice as small (ht/2)
    int ct = 30; //center threshold, votes
    int minRad = 80; //minimum considered detection
    int maxRad = 150;
    int mdd = 30; //min distance denominator: what the min distance between centers is divided into (larger value = smaller mindist)
    bool morethanq = false; //there are coins higher in value than quarter
    cout << argc;
    for(int i =0; i<argc; i++){ 
        if(strcmp(argv[i], "-f") == 0){
            image = imread(argv[i+1],1);
            im =imread(argv[i+1],1);
            gray = imread(argv[i+1],IMREAD_GRAYSCALE); //grayscale input image
            cout << "file processed";
        }
        if(strcmp(argv[i], "-ht") == 0){ //cannyedge thresh
            ht = stoi(argv[i+1]);
        }
        if(strcmp(argv[i], "-ct") == 0){ //center voting thresh
            ct = stoi(argv[i+1]);
        }
        if(strcmp(argv[i], "-minr") == 0){ //minimum radius detected by hough circles
            minRad = stoi(argv[i+1]);
        }
        if(strcmp(argv[i], "-maxr") == 0){ //maximum radius 
            maxRad = stoi(argv[i+1]);
        }
        if(strcmp(argv[i], "-mdd") == 0){
            mdd = stoi(argv[i+1]);
        }
        if(strcmp(argv[i], "-highestcoin") == 0){
            if(strcmp(argv[i+1], "quarter") !=0){
                morethanq = true;
            }
        }
    }
    imwrite("./imageg.jpg", gray); //create grayscale image
    
    medianBlur(gray, gray, 5);
    GaussianBlur(gray, gray, Size(3, 3), 0, 0, BORDER_DEFAULT);
    //canny edge
    Mat edges, cannyout;
    Canny(gray, cannyout, ht/1.4, ht, 3); //grayscale image, edges out, low thresh, high thresh, sobel kernel (3x3)
    edges = Scalar::all(0);
    gray.copyTo(edges, cannyout);
    imwrite("./imagef.jpg", edges);
  //  hough transform: identify the centers and radiuses using OpenCV and hough transform
    vector<Vec3f> circles;
    HoughCircles(gray, circles, HOUGH_GRADIENT, 1, //grayscale image, vector w xyrad for circles, gradient, inverse resolution ratio, min distance between centers, threshold for cannyedge, threshold for centers, minrad, maxrad;
                 gray.rows/mdd,  
                 ht, ct, minRad, maxRad);
    int maxdetectrad = 0; //the biggest detected radius
    for( size_t i = 0; i < circles.size(); i++ ) //display centers and outlines
    {
        Vec3i c = circles[i];
        Point center = Point(c[0], c[1]); // c = h, k, rad
        // circle center: #circle(image, center, 1, Scalar(0,100,100), 3, LINE_AA);
        int radius = c[2];
        if(radius>maxdetectrad){
            maxdetectrad = radius;
        }
        //pennies red, quarters purple, nickel yellow
        circle(image, center, radius, Scalar(0,0,255), 4, LINE_AA); //detected circles in red, thickness = 4 TEMPORARILY BLACK
    }
    imwrite("./imageCircles.jpg",image);
    int pennycount = 0;
    int nickelcount= 0; 
    int dimecount= 0;
    int quartercount= 0; 
    int halfdolcount = 0; 
    int silvercount = 0;
    for( size_t i = 0; i < circles.size(); i++ ) //display centers and outlines
    {
        Vec3i c = circles[i];
        Point center = Point(c[0], c[1]); // c = h, k, rad
        cout<<"rad: "<<c[2]<<"\n";
        // circle center: #circle(image, center, 1, Scalar(0,100,100), 3, LINE_AA);
        int radius = c[2];
        //pennies red, quarters purple, nickel yellow
        circle(image, center, radius, Scalar(0,0,255), 4, LINE_AA); //detected circles in red, thickness = 4 TEMPORARILY BLACK
        int r = image.at<Vec3b>(c[1], c[0])[2];//getting the pixel values//
        if(!morethanq){ //categorizing
            if(radius >=0.9*maxdetectrad){ //quarter = purple
            circle(image, center, radius, Scalar(255,0,150), 4, LINE_AA); 
            quartercount+=1;
            }
            else if(radius>=0.84*maxdetectrad){ //nickels fo sho 
                circle(image, center, radius, Scalar(0,255,255), 4, LINE_AA); //yellow 
                nickelcount+=1;
            }
            else{ //separate nickels dimes and pennies
                vector<int> rgb = avg_rgb(c[0],c[1],im);
                int r = rgb[0]; int g = rgb[1]; int b = rgb[2];
                if(r-(g+b)/2 > 20 or(r+g+b)/3 <=65){ //pennies, either red or super dark
                    circle(image, center, radius, Scalar(0,0,255), 4, LINE_AA);
                    pennycount+=1;
                }
                else if(radius<.69*maxdetectrad){ //dime blue
                    circle(image, center, radius, Scalar(255,0,0), 4, LINE_AA);
                    dimecount+=1;
                }
                else{
                    circle(image, center, radius, Scalar(0,255,255), 4, LINE_AA);
                    nickelcount+=1;
                }
            }
        } else{
            cout<<"hard"<<"\n";
            if(radius>0.95*maxdetectrad){ //one/silver dollar, pink
                circle(image, center, radius, Scalar(255,0,255), 4, LINE_AA); 
                silvercount+=1;
            }
            else if(radius>0.7*maxdetectrad){ //half dollar
                circle(image, center, radius, Scalar(0,255,0), 4, LINE_AA); 
                halfdolcount+=1;
            }
            else if(radius >=0.63*maxdetectrad){ //quarter = purple
                circle(image, center, radius, Scalar(255,0,150), 4, LINE_AA); 
                quartercount+=1;
            }
            else if(radius>=0.54*maxdetectrad){ //nickels fo sho 
                circle(image, center, radius, Scalar(0,255,255), 4, LINE_AA); //yellow 
                nickelcount+=1;
            }
            else{ //separate nickels dimes and pennies
                vector<int> rgb = avg_rgb(c[0],c[1],im);
                int r = rgb[0]; int g = rgb[1]; int b = rgb[2];
                if(r-(g+b)/2 > 20 or(r+g+b)/3 <=65){ //pennies, either red or super dark
                    circle(image, center, radius, Scalar(0,0,255), 4, LINE_AA);
                    pennycount+=1;
                }
                else if(radius<.45*maxdetectrad){ //dime blue
                    circle(image, center, radius, Scalar(255,0,0), 4, LINE_AA);
                    dimecount+=1;
                }
                else{
                    circle(image, center, radius, Scalar(0,255,255), 4, LINE_AA);
                    nickelcount+=1;
                }
            }
        }
    }
    imwrite("./imageCoins.jpg", image);
    //generate text file with cost
    ofstream outfile("results.txt");
    outfile<<"Detected Change: \n"<<silvercount<<" silver coins, "<<halfdolcount<<" half dollars, "<<quartercount<<" quarters, "<<
        nickelcount<<" nickels, "<<dimecount<<" dimes, and "<<pennycount<<" pennies. \n";
    cout<<"Detected Change: \n"<<silvercount<<" silver coins, "<<halfdolcount<<" half dollars, "<<quartercount<<" quarters, "<<
        nickelcount<<" nickels, "<<dimecount<<" dimes, and "<<pennycount<<" pennies. \n";
    double total = silvercount+ 0.5*halfdolcount + .25*quartercount + .05*nickelcount + 0.1*dimecount + 0.01*pennycount;
    outfile<<"Total: $"<<total<<"\n";
    cout<<"Total: $"<<total<<"\n";
    outfile.close();
    waitKey(0);
    return 0;
    
}*/

