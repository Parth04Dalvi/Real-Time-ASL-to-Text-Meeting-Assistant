// This script runs automatically on Google Meet/Zoom pages
const overlay = document.createElement('div');
overlay.id = 'asl-assistant-overlay';
document.body.appendChild(overlay);

// Use a Shadow DOM to prevent the meeting site's CSS from breaking your app
const shadow = overlay.attachShadow({ mode: 'open' });
const root = document.createElement('div');
shadow.appendChild(root);

// Inject your React App into 'root'
// (When you build your React app, it will bundle into a single JS file)
console.log("ASL Assistant Injected into Meeting");
