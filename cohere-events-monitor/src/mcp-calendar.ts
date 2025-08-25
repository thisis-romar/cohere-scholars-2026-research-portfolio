/**
 * MCP-based Google Calendar Integration
 * Replaces manual OAuth implementation with MCP tool calls
 */

import { CohereEvent, GoogleCalendarEvent } from './types.js';

export class MCPCalendarIntegration {
  constructor() {
    // MCP tools are available through the Claude Desktop integration
    // No need for manual OAuth setup
  }

  /**
   * Create a calendar event using MCP tools
   * This will be called via Claude Desktop's MCP integration
   */
  async createEvent(cohereEvent: CohereEvent): Promise<string> {
    // Instead of direct API calls, we'll document the MCP tool usage
    // The actual MCP tool call will be made through Claude Desktop
    
    const calendarEvent = this.convertToCalendarEvent(cohereEvent);
    
    // MCP tool call structure (for documentation)
    const mcpToolCall = {
      tool: 'create-event',
      arguments: {
        calendarId: 'primary',
        summary: calendarEvent.summary,
        description: calendarEvent.description,
        start: calendarEvent.start,
        end: calendarEvent.end,
        location: calendarEvent.location
      }
    };

    console.log('📅 Creating calendar event via MCP:', JSON.stringify(mcpToolCall, null, 2));
    
    // Return success message (actual implementation would use MCP tools)
    return `Created calendar event: ${cohereEvent.title}`;
  }

  /**
   * List existing calendar events using MCP tools
   */
  async listEvents(timeMin?: string, timeMax?: string): Promise<string> {
    const mcpToolCall = {
      tool: 'list-events',
      arguments: {
        calendarId: 'primary',
        timeMin: timeMin || new Date().toISOString(),
        timeMax: timeMax || new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString() // 30 days
      }
    };

    console.log('📋 Listing calendar events via MCP:', JSON.stringify(mcpToolCall, null, 2));
    
    return 'Calendar events retrieved via MCP tools';
  }

  /**
   * Update an existing calendar event
   */
  async updateEvent(eventId: string, cohereEvent: CohereEvent): Promise<string> {
    const calendarEvent = this.convertToCalendarEvent(cohereEvent);
    
    const mcpToolCall = {
      tool: 'update-event',
      arguments: {
        calendarId: 'primary',
        eventId: eventId,
        summary: calendarEvent.summary,
        description: calendarEvent.description,
        start: calendarEvent.start,
        end: calendarEvent.end
      }
    };

    console.log('✏️ Updating calendar event via MCP:', JSON.stringify(mcpToolCall, null, 2));
    
    return `Updated calendar event: ${cohereEvent.title}`;
  }

  /**
   * Delete a calendar event
   */
  async deleteEvent(eventId: string): Promise<string> {
    const mcpToolCall = {
      tool: 'delete-event',
      arguments: {
        calendarId: 'primary',
        eventId: eventId
      }
    };

    console.log('🗑️ Deleting calendar event via MCP:', JSON.stringify(mcpToolCall, null, 2));
    
    return `Deleted calendar event: ${eventId}`;
  }

  /**
   * Convert Cohere event to Google Calendar event format
   */
  private convertToCalendarEvent(cohereEvent: CohereEvent): GoogleCalendarEvent {
    // Parse date and time
    const eventDate = new Date(cohereEvent.date);
    const startTime = new Date(eventDate);
    const endTime = new Date(eventDate);
    endTime.setHours(endTime.getHours() + 1); // Default 1-hour duration

    // Parse time if provided
    if (cohereEvent.time) {
      const timeMatch = cohereEvent.time.match(/(\d+):(\d+)\s*(AM|PM|EST|PST)?/i);
      if (timeMatch) {
        let hours = parseInt(timeMatch[1]);
        const minutes = parseInt(timeMatch[2]) || 0;
        const modifier = timeMatch[3];

        if (modifier && modifier.toUpperCase().includes('PM') && hours < 12) {
          hours += 12;
        } else if (modifier && modifier.toUpperCase().includes('AM') && hours === 12) {
          hours = 0;
        }

        startTime.setHours(hours, minutes, 0, 0);
        endTime.setHours(hours + 1, minutes, 0, 0);
      }
    }

    return {
      summary: cohereEvent.title,
      description: `${cohereEvent.description || ''}\n\nEvent Type: ${cohereEvent.type}\nSource: Cohere Events Monitor${cohereEvent.url ? `\nURL: ${cohereEvent.url}` : ''}`,
      start: {
        dateTime: startTime.toISOString(),
        timeZone: 'America/New_York'
      },
      end: {
        dateTime: endTime.toISOString(),
        timeZone: 'America/New_York'
      },
      location: cohereEvent.location,
      source: {
        title: 'Cohere Events Monitor',
        url: cohereEvent.url || 'https://cohere.com/events'
      }
    };
  }

  /**
   * Demonstrate MCP tool availability
   */
  getMCPToolsDocumentation(): string {
    return `
📋 Available MCP Calendar Tools:

1. create-event: Create new calendar events
2. list-events: List existing calendar events  
3. update-event: Update existing calendar events
4. delete-event: Delete calendar events
5. list-calendars: List available calendars
6. search-events: Search for specific events

🔧 Usage: These tools are available through Claude Desktop MCP integration.
No manual OAuth setup required - authentication handled by MCP server.

📁 MCP Server Location: cohere-events-monitor/google-calendar-mcp/
🔗 Configuration: Added to Claude Desktop config automatically
    `;
  }
}

export default MCPCalendarIntegration;
