const { exec } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const currentDir = process.cwd();
const saveDir = path.join(currentDir, 'References', 'Videos', 'attachments');

if (!fs.existsSync(saveDir)) {
	fs.mkdirSync(saveDir, { recursive: true });
}

const runCommand = (command) => {
	return new Promise((resolve, reject) => {
		exec(command, (error, stdout, stderr) => {
			if (error) {
				reject(error);
			} else {
				resolve(stdout);
			}
		});
	});
};

const compressFile = async () => {};

const generateUUID = () => {
	return crypto.randomUUID();
};

async function saveAudio(url) {
	const uuid = generateUUID();
	const outputFilename = `ref-${uuid}.mp3`;
	return `successfully hit saveAudio user script with URL: ${url}`;
	// Download audio only from the video using yt-dlp
	const downloadAudioCmd = `yt-dlp -f "ba[ext=m4a]" -o "ref-${uuidStr}.%(ext)s" ${videoUrl}`;
	await runCommand(downloadAudioCmd);
}
module.exports = saveAudio;

async function saveVideo(url) {
	const uuid = generateUUID();
	const outputFilename = `ref-${uuid}.mp4`;
	const downloadCmd = `yt-dlp -f "bestvideo*[height<=1080][ext=mp4]+bestaudio*[ext=m4a]/best[ext=mp4]/best" -o "${outputFilename}" ${url}`;
	await runCommand(downloadCmd);
	// return outputFilename;
	return `successfully hit saveVideo user script with URL: ${url}`;
}
module.exports = saveVideo;

const convertVideoToGif = async () => {
	// GIF parameters
	const fpsValues = [12];
	const speedValues = [2];
	const scaleValues = [480];

	// Compression parameters
	const lossyValues = [90];
	const colorValues = [128];

	for (const fps of fpsValues) {
		for (const speed of speedValues) {
			for (const scaleWidth of scaleValues) {
				if (fs.existsSync(`ref-${uuidStr}.mkv`)) {
					ext = 'mkv';
				}
				if (fs.existsSync(`ref-${uuidStr}.mp4`)) {
					ext = 'mp4';
				}

				// Convert the downloaded video to a GIF
				const vid2gifCmd = `ffmpeg -i "ref-${uuidStr}.${ext}" -filter:v "fps=${fps},setpts=${
					1 / speed
				}*PTS,scale=${scaleWidth}:-1" -y "ref-${uuidStr}-speed_${speed}x-FPS_${fps}-w${scaleWidth}.gif"`;
				await runCommand(vid2gifCmd);
				outputString += '\nVideo to GIF conversion complete.';

				if (isGifCompress === '1') {
					for (const lossy of lossyValues) {
						for (const color of colorValues) {
							// Compress the GIF
							const compressCmd = `gifsicle -O3 --lossy=${lossy} --colors ${color} "ref-${uuidStr}-speed_${speed}x-FPS_${fps}-w${scaleWidth}.gif" -o "ref-${uuidStr}-speed_${speed}x-FPS_${fps}-w${scaleWidth}-compressed-lossy_${lossy}-colors_${color}.gif"`;
							await runCommand(compressCmd);
							outputString += '\nGIF compression complete.';
						}
					}
				}
			}
		}
	}
};
