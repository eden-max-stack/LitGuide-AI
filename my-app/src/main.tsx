import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import { ConvexProvider, ConvexReactClient } from 'convex/react';

// Initialize Convex client with your deployment URL
const convex = new ConvexReactClient(import.meta.env.VITE_CONVEX_URL as string);

// Create the root and render your application once
const rootElement = document.getElementById('root');

if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <StrictMode>
      <ConvexProvider client={convex}>
        <App />
      </ConvexProvider>
    </StrictMode>
  );
}
