# Ananya Karn - Portfolio

Personal portfolio website built with Vite, showcasing engineering projects, cloud infrastructure expertise, and systems thinking.

## 🚀 Live Demo
The site is automatically deployed to GitHub Pages. You can find the link in your repository settings under **Settings > Pages**.

## 🛠️ Tech Stack
- **Framework**: Vite
- **Styling**: Vanilla CSS (Custom tokens)
- **Logic**: Vanilla JavaScript
- **Deployment**: GitHub Actions

## 💻 Local Development

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd kripinya
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

4. **Build for production**:
   ```bash
   npm run build
   ```

## 📦 Deployment Instructions

This project uses **GitHub Actions** for automatic deployment. Every time you push to the `main` branch, the site is rebuilt and deployed to the `gh-pages` branch.

### Prerequisites for GitHub Pages:
1. Go to your repository on GitHub.
2. Navigate to **Settings > Actions > General**.
3. Under **Workflow permissions**, select **Read and write permissions** and click **Save**.
4. In **Settings > Pages**, ensures the source is set to "Deploy from a branch" and select `gh-pages` (folder `/root`).

## 📁 Project Structure
- `index.html`: Entry point.
- `main.js`: Core interactivity and animations.
- `style.css`: Global styles.
- `src/tokens.css`: Design system variables.
- `public/`: Static assets.
