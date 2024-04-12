CREATE TABLE IF NOT EXISTS `tfrs` (
    `tfr_id` int(11) NOT NULL,
    `company_name` varchar(255) NOT NULL,
    `rocket_name` varchar(255) NOT NULL,
    `date` varchar(255) NOT NULL,
    `time_utc` varchar(255) NOT NULL,
    `area` varchar(255) NOT NULL,
    `reason` varchar(255) NOT NULL,
    `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);