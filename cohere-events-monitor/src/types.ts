/**
 * Core TypeScript interfaces for Cohere Events Monitoring System
 * Provides type safety and structure for event data and system configuration
 */

export interface CohereEvent {
  id: string;
  title: string;
  date: string;
  time?: string;
  description?: string;
  location?: string;
  url?: string;
  type: 'research' | 'general' | 'workshop' | 'conference';
  tags?: string[];
}

export interface MonitorConfig {
  checkInterval: string; // cron format
  googleCalendarId?: string;
  enableNotifications: boolean;
  outputPath?: string;
  logLevel: 'debug' | 'info' | 'warn' | 'error';
}

export interface SyncState {
  lastCheck: Date;
  eventsFound: number;
  eventsAdded: number;
  eventsUpdated: number;
  errors: string[];
}

export interface GoogleCalendarEvent {
  summary: string;
  description?: string;
  start: {
    dateTime?: string;
    date?: string;
    timeZone?: string;
  };
  end: {
    dateTime?: string;
    date?: string;
    timeZone?: string;
  };
  location?: string;
  source?: {
    title: string;
    url: string;
  };
}

export interface MCPFirecrawlResponse {
  markdown?: string;
  html?: string;
  metadata?: {
    title?: string;
    description?: string;
    language?: string;
    sourceURL?: string;
  };
}
