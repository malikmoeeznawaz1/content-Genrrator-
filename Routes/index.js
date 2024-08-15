const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const { HfInference } = require("@huggingface/inference");

// const inference = new HfInference('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');

router.get('/', (req, res) => {
    res.render('index');
});

router.post('/generate', (req, res) => {
    const { prompt } = req.body;
    console.log('Prompt:', prompt);
    
    // Call the Python script
    exec(`python model_inference.py "${prompt}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ error: 'Failed to generate text' });
        }

        try {
            const response = JSON.parse(stdout);
            const generatedText = response.generated_text || 'No text generated';

            // Render the EJS view with the generated text
            res.render('index', { generatedText });
        } catch (parseError) {
            console.error('Error parsing Python script output:', parseError);
            res.status(500).json({ error: 'Failed to parse Python script output' });
        }
    });
});

module.exports = router;
