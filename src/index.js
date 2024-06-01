const axios = require('axios');
const readability = require('@mozilla/readability');
const puppeteer = require('puppeteer');
const { JSDOM } = require('jsdom');
const fs = require('fs');

// URL to scrape
const url = 'https://wutheringwaves.fandom.com/wiki/Category:Characters';

(async () => {
    // Launch Puppeteer
    const browser = await puppeteer.launch();
    // Open a new page
    const page = await browser.newPage();
    // Go to the URL
    await page.goto(url);
    // Wait for the page to load
    await page.waitForSelector('a.category-page__member-link');
    // Get the links
    let div_selector = 'a.category-page__member-link';
    // Evaluate the links
    let links = await page.evaluate((sel) => {
        let elements = Array.from(document.querySelectorAll(sel));
        let links = elements.map((element) => {
            return element.href;
        });
        return links;
    }, div_selector);
    // Loop through the links
    for (let i = 0; i < links.length; i++) {
        // Use axios to fetch the page
        const response = await axios.get(links[i]);
        const doc = new JSDOM(response.data, { url: links[i] });
        // Use Readability to parse the article and extract the content
        const reader = new readability.Readability(doc.window.document);
        const article = reader.parse();
        // Save the article to a file
        fs.writeFileSync(
            `./output/${article.title
                .replace(/\s/g, '_')
                .replace(/[^a-zA-Z0-9]/g, '')}.txt`,
            article.excerpt ? article.excerpt : ''
        );
    }
    // Close the browser
    await browser.close();
})();
