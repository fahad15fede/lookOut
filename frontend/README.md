# lookOut Frontend

Modern security monitoring dashboard for the lookOut home security system.

## Tech Stack

- React 18
- React Router DOM
- Vite
- JavaScript (JSX)
- CSS

## Project Structure

```
src/
├── api/
│   └── events.js           # API client for backend communication
├── components/
│   ├── EventCard.jsx       # Individual event display card
│   ├── EventList.jsx       # Grid of event cards
│   ├── Header.jsx          # Application header with status
│   ├── Sidebar.jsx         # Navigation sidebar
│   ├── StatCard.jsx        # Dashboard statistics card
│   └── StatusBadge.jsx     # System status indicator
├── pages/
│   ├── Dashboard.jsx       # Main dashboard page
│   └── Events.jsx          # All events page with filtering
├── utils/
│   ├── dateUtils.js        # Date formatting utilities
│   └── statsUtils.js       # Statistics calculation
├── App.jsx                 # Root component with routing
├── main.jsx                # Application entry point
├── App.css                 # App layout styles
└── index.css               # Global styles
```

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file (copy from `.env.example`):
```bash
VITE_API_URL=http://localhost:8000
```

3. Start development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

5. Lint code:
```bash
npm run lint
```

## Features

### Dashboard
- Real-time system status indicator
- Statistics cards (total events, today's events, latest track ID, system status)
- Recent intrusions display (last 6 events)
- Manual refresh button
- Error handling for backend unavailability

### Events Page
- View all security events
- Filter by time (All / Today)
- Search by Track ID
- Manual refresh button

### Event Cards
- Intrusion crop image display
- Event details (ID, track ID, date, time)
- View full evidence link
- Fallback for missing images

## API Integration

The frontend communicates with the FastAPI backend running at `http://localhost:8000`.

### Endpoints Used
- `GET /api/events` - Fetch all intrusion events
- `GET /evidence/{filename}` - Fetch evidence images

### Data Flow
1. User opens dashboard/events page
2. Component calls `getEvents()` from `api/events.js`
3. API response is stored in component state
4. Statistics are calculated client-side using `statsUtils.js`
5. Events are rendered using `EventCard` components
6. Evidence URLs are constructed using `getEvidenceUrl()` helper
7. Images are fetched directly from backend static file endpoint

## Evidence URL Construction

Backend stores Windows paths like:
```
recordings\intrusions\intrusion_2026-09-26_02-37-11_id-3_crop.jpg
```

Frontend extracts filename and constructs URL:
```
http://localhost:8000/evidence/intrusion_2026-09-26_02-37-11_id-3_crop.jpg
```

## Environment Variables

- `VITE_API_URL` - Backend API base URL (default: `http://localhost:8000`)

## Browser Support

Modern browsers with ES6+ support.
