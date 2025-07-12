from datetime import datetime

def log_crm_heartbeat():
    # Log a heartbeat message to confirm the CRM application is running.
    # This function is called every 5 minutes by django-crontab.
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
        
        # Log the heartbeat message
        log_message = f"{timestamp} CRM is alive\n"
        
        # Write to log file
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(log_message)
            
        return "Heartbeat logged successfully"
    except Exception as e:
        # If there's an error, log it to the same file
        error_message = f"{timestamp} Error in CRM heartbeat: {str(e)}\n"
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(error_message)
        return f"Error: {str(e)}"
