INSTALLED_APPS += [
    'djangocrontab',
]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron_jobs.update_low_stock'),
]
