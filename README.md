# Wallpaper Gallery

A trial project for exploring and learning GitHub Actions workflows. This project demonstrates how to build an automated wallpaper collection gallery that syncs daily Bing wallpapers and displays them in an interactive web interface.

## Features

This trial project showcases key GitHub Actions capabilities:

- 🤖 **GitHub Actions Workflow** - Automated daily sync using cron schedules
- 📅 **Data Pipeline** - Fetching, processing, and storing data automatically
- 🔄 **Continuous Integration** - Auto-commit and push on successful runs
- 📦 **JSON Data Management** - Parsing and updating JSON with jq
- 🖼️ **Responsive Gallery** - Beautiful grid layout that adapts to all screen sizes
- 🎨 **Modern UI** - Built with Tailwind CSS for a clean, professional look
- 🖱️ **Interactive Preview** - Click any wallpaper to view full-size in a modal
- ⚡ **Lazy Loading** - Images load on-demand for optimal performance

## Project Structure

```
wallpaper_gallery/
├── .github/
│   └── workflows/
│       └── sync-wallpapers.yml    # GitHub Actions workflow for daily sync
├── wallpapers/
│   ├── database.json              # JSON database of all wallpapers
│   └── *.jpg                      # Wallpaper image files
├── index.html                     # Main gallery website
└── README.md                      # This file
```

## Technologies Used

- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Backend**: Bash (GitHub Actions), jq (JSON processing)
- **API**: Bing Image Archive API
- **Version Control**: Git & GitHub
- **CI/CD**: GitHub Actions Workflows

## About This Trial Project

This project was created as a **learning experiment** to understand and implement:

- **GitHub Actions**: Setting up automated workflows with scheduled triggers
- **Workflow Triggers**: Using cron schedules for daily automation
- **Data Pipeline**: Fetching external API data and processing it
- **File Manipulation**: Using bash and jq to parse and update JSON
- **Git Automation**: Automatically committing and pushing changes from workflows
- **Error Handling**: Preventing duplicate entries and handling missing files
- **Workflow Permissions**: Managing write access for automated commits

The actual wallpaper gallery is a practical demonstration of these concepts in action. It's a fully functional project that serves as a great reference for anyone learning GitHub Actions!

## Getting Started

### Prerequisites

- Git
- A web browser (no server required for basic viewing)
- GitHub account (for automated syncing)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/wallpaper_gallery.git
   cd wallpaper_gallery
   ```

2. **View the gallery locally**
   - Option A: Open `index.html` directly in your browser
   - Option B: Serve locally with Python:
     ```bash
     python -m http.server 8000
     ```
     Then visit `http://localhost:8000`

## How It Works

### The GitHub Actions Workflow (Learning Showcase)

The `.github/workflows/sync-wallpapers.yml` file is the **core learning component** of this trial project. It demonstrates:

- **Scheduled Triggers**: Uses cron syntax (`0 0 * * *`) to run daily at midnight UTC
- **Manual Triggers**: `workflow_dispatch` allows manual execution via GitHub UI
- **Permissions Management**: Sets `contents: write` for git operations
- **External API Integration**: Fetches data from Bing's Image Archive API using curl
- **JSON Processing**: Uses jq for safe JSON parsing and manipulation
- **File Operations**: Downloads images and manages file structure
- **Bash Scripting**: Complete data pipeline in shell script
- **Git Automation**: Configures git identity and auto-commits changes
- **Conditional Logic**: Prevents duplicate entries and detects changes

### The Complete Workflow Execution

Each automated run performs these steps:

1. **Checkout** - Retrieves the repository using `actions/checkout@v4`
2. **Fetch Data** - Calls Bing's API to get the latest wallpaper metadata
3. **Extract Fields** - Uses jq to safely parse JSON response
4. **Download Image** - Stores the image with a formatted filename
5. **Update Database** - Prepends new entry to `database.json` (if unique date)
6. **Smart Commits** - Only commits if there are actual changes
7. **Push Changes** - Automatically updates the repository

This demonstrates a **complete data pipeline** from external API to version-controlled storage!

### Database Format

Each wallpaper entry in `wallpapers/database.json` follows this structure:

```json
{
  "date": "2026-02-17",
  "title": "Beautiful Landscape Title",
  "copyright": "© Photo Credit",
  "url": "wallpapers/YYYY-MM-DD - Title.jpg"
}
```

### Gallery Display

The `index.html` file:
- Fetches and parses `database.json`
- Groups wallpapers by date
- Displays them in a responsive grid
- Formats dates for readability
- Shows wallpaper count per date
- Lazy-loads images for performance

## Usage

### Viewing the Gallery

1. Open `index.html` in your web browser
2. Browse wallpapers organized by date
3. Click any image to view full-size
4. Hover for interactive effects
5. Close preview by clicking outside the image or the ✕ button

### Adding Manual Entries

Edit `wallpapers/database.json` and add entries with the same structure:

```json
{
  "date": "YYYY-MM-DD",
  "title": "Your Wallpaper Title",
  "copyright": "Your Copyright Info",
  "url": "wallpapers/your-image.jpg"
}
```

### Experimenting with the Workflow (Learning)

Edit `.github/workflows/sync-wallpapers.yml` to learn and experiment:

**Schedule Changes**
- Change frequency: `cron: '0 */6 * * *'` (every 6 hours)
- Run on multiple triggers: Add `push:` or `pull_request:`
- Test with `workflow_dispatch` for manual testing

**Data Processing Learning**
- Modify jq queries to extract different fields
- Add additional processing steps
- Experiment with conditional logic using bash `if` statements

**API Exploration**
- Try different Bing API parameters (idx, n, mkt)
- Fetch multiple images instead of one
- Combine data from multiple sources

**Git Automation**
- Change commit message format
- Add tags for each sync
- Push to different branches for different purposes

**Error Handling**
- Add validation checks
- Create notifications for failures
- Log detailed information for debugging

## GitHub Actions Workflow Details

**Trigger Events:**
- `schedule`: Daily at 00:00 UTC (adjust cron as needed)
- `workflow_dispatch`: Manual trigger via GitHub UI

**Permissions Required:**
- `contents: write` - To commit changes to the repository

**Main Steps:**
1. Checkout repository
2. Fetch and process Bing wallpaper
3. Update database with new entry (if unique date)
4. Commit and push changes

## Development

### Making Changes to the Gallery

The gallery is built with vanilla HTML, CSS (Tailwind), and JavaScript - no build process required!

**To modify:**
- Gallery layout: Edit the grid classes in `index.html`
- Colors/styling: Customize Tailwind classes
- API data source: Modify workflow script
- Database structure: Update all three files consistently

### Testing Locally

1. Modify `database.json` with test data
2. Open `index.html` in browser
3. Check console (F12) for any errors
4. Test responsiveness with browser dev tools

## Troubleshooting

### Images not loading?
- Check file paths in `database.json`
- Ensure images exist in `wallpapers/` folder
- Verify relative paths are correct

### Workflow not running?
- Check GitHub Actions tab for logs
- Verify workflow file syntax (must be valid YAML)
- Ensure `.github/workflows/` directory exists

### JSON parse errors?
- Validate JSON format using `jq` or an online validator
- Check for unescaped quotes in titles
- Ensure proper formatting with commas and brackets

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Considerations

- Images are lazy-loaded for faster page loads
- Grid layout is responsive and optimized
- Modal images fade in smoothly
- Hover effects use GPU-accelerated transforms

## Future Enhancements & Learning Opportunities

This trial project can be extended to learn more GitHub Actions concepts:

### Gallery Features
- [ ] Add search/filter functionality
- [ ] Implement favorites/bookmarking
- [ ] Add download buttons
- [ ] Create dark/light mode toggle
- [ ] Add metadata display (copyright, photographer)

### GitHub Actions Learning Extensions
- [ ] **Matrix Builds**: Fetch from multiple image sources simultaneously
- [ ] **Workflows with Dependencies**: Chain multiple jobs together
- [ ] **Artifact Handling**: Generate reports or statistics files
- [ ] **Secrets Management**: Use encrypted environment variables for API keys
- [ ] **Notifications**: Send alerts on workflow success/failure
- [ ] **Testing**: Add validation tests before commits
- [ ] **Conditional Workflows**: Run different jobs based on conditions
- [ ] **Reusable Workflows**: Extract common logic into workflow templates
- [ ] **Auto-labeling**: Use actions to automatically label issues/PRs
- [ ] **Release Automation**: Auto-generate releases with workflow artifacts

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## Learning Resources

This trial project demonstrates concepts from:

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Scheduled Workflows & Cron](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule)
- [jq Manual](https://stedolan.github.io/jq/)
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [Bing Wallpaper API](https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US)

## Credits

- **Project Type**: GitHub Actions Trial/Learning Project
- Wallpapers sourced from [Bing Image Archive](https://www.bing.com/gallery/)
- UI built with [Tailwind CSS](https://tailwindcss.com/)
- CI/CD powered by [GitHub Actions](https://github.com/features/actions)
- JSON processing with [jq](https://stedolan.github.io/jq/)

## Support

For issues and questions:
1. Check existing GitHub issues
2. Review the troubleshooting section above
3. Create a new issue with details

---

## Project Status

🧪 **TRIAL PROJECT** - This repository is an experimental learning platform for GitHub Actions workflows. While the wallpaper gallery is fully functional, the primary goal is to demonstrate and document GitHub Actions capabilities and best practices.

Feel free to fork, experiment, and use this as a reference for your own GitHub Actions projects!

**Last Updated:** February 17, 2026
