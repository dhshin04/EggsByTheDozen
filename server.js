const express = require('express');
const app = express();

/* Multer Middleware for File Uploads */
const multer = require('multer');
const upload = multer({
	limits: { fileSize: 10 * 1024 * 1024 },	// 50 MB file size limit 
	dest: 'uploads/' 
});		// Instance of multer

/* Executes Child Process on Shell */
const { exec } = require('child_process');

/* Handles File Removal */
const { unlink } = require('fs');

/* Middleware for Static Files */
app.use(express.static('static'));

/* Path to MyProject - changes based on OS */
const path = require('path');
const myProjectPath = path.join('static', 'images', 'imParasites.png');		// try join('images', 'imParasites.png') if this doesn't work

/* View .ejs format */
app.set('view engine', 'ejs');


/* GET and POST requests */
app.get('/', (req,res) => {
	// Render index.ejs without fecal egg count
	res.render("index.ejs", { show: false, count: -1, image: '' });
});

// upload.single() saves image in 'upload/' path
app.post('/', upload.single("image"), (req,res) => {
	const imagePath = req.file.path;		// Path to client's image input

	// Execute OpenCV executable file
	exec(`python main.py -f ${imagePath}`, (error, stdout, stderr) => {
		// Error with executing - terminate exec()
		if (error) {
			console.log("Error: " + stderr);
			res.status(500).send('Failed to process image sent by client: ' + stderr);

			// Remove image from uploads/
			unlink(imagePath, err => {
				if (err) {
					console.log("Failed to remove image from 'uploads/' path");
				}
			});
			return;
		}

		let result = stdout;
		result = result.replace('Seen: ', '');
		result = result.replace('Eggs Per Gram: ', '');
		let tokenIndex = result.indexOf('\n');
		let fec = result.substring(0, tokenIndex);
		let epg = result.substring(tokenIndex + 1);

		// Render index.ejs with fecal egg count
		res.render("index.ejs", { show: true, count: fec, gram: epg, image: 'imParasites.png' });

		// Remove image from uploads/
		unlink(imagePath, error => {
			if (error) {
				console.log("Failed to remove image from 'uploads/' path");
			}
		});
	});
})

// Start the server - listen from all IP (0.0.0.0)
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => console.log(`Server running on port ${PORT}`));