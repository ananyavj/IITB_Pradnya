import React from 'react'
import ReactDOM from 'react-dom/client'
import { MantineProvider } from '@mantine/core'
import '@mantine/core/styles.css'
import App from './App.tsx'
import './index.css'
import { Workbox } from 'workbox-window'

if ('serviceWorker' in navigator) {
    const wb = new Workbox('/sw.js')
    wb.register()
}

ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <MantineProvider>
            <App />
        </MantineProvider>
    </React.StrictMode>,
)
