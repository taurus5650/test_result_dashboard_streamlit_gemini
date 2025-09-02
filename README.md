# automation_test_result_dashboard


```sql
CREATE TABLE IF NOT EXISTS automation_test_result (
    id SERIAL PRIMARY KEY,
    service TEXT NOT NULL,
    service_team TEXT NOT NULL, -- The dev team
    request_id TEXT,
    is_rerun BOOLEAN DEFAULT FALSE,
    trigger_status INT NOT NULL, -- 0=start, 1=success, 2=failed (infra down etc.), 99=unknown
    trigger_type INT NOT NULL, -- 0=manual, 1=dailyAutomation, 3=ci/cd
    trigger_user TEXT,

    case_total_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    skip_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    broken_count INTEGER DEFAULT 0,
    all_test_records JSONB, -- Record TC name, status (passed, failed, skipped, broken), duration, tags
    failure_records JSONB, -- Record TC's failure details

    duration FLOAT DEFAULT 0, -- Overall testing duration
    start_time TIMESTAMP,
    end_time TIMESTAMP,

    create_time TIMESTAMP DEFAULT NOW(),
    update_time TIMESTAMP DEFAULT NOW()
);
```