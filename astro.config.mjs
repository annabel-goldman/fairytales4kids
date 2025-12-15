import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  // Your custom domain - update this if you use a different domain
  // For GitHub Pages with custom domain:
  site: 'https://fairytales4kids.com',
  
  // If deploying to a GitHub Pages project site (username.github.io/repo-name),
  // uncomment and update the base path:
  // base: '/repo-name',
  
  build: {
    assets: 'assets'
  },
  
  // Ensure static output for GitHub Pages
  output: 'static'
});
