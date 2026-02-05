CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY,
    creator_id UUID NOT NULL,
    video_created_at TIMESTAMP NOT NULL,
    views_count BIGINT NOT NULL DEFAULT 0,
    likes_count BIGINT NOT NULL DEFAULT 0,
    comments_count BIGINT NOT NULL DEFAULT 0,
    reports_count BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS video_snapshots (
    id SERIAL PRIMARY KEY,
    video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL,
    views_count BIGINT NOT NULL DEFAULT 0,
    likes_count BIGINT NOT NULL DEFAULT 0,
    comments_count BIGINT NOT NULL DEFAULT 0,
    reports_count BIGINT NOT NULL DEFAULT 0,
    delta_views_count BIGINT NOT NULL DEFAULT 0,
    delta_likes_count BIGINT NOT NULL DEFAULT 0,
    delta_comments_count BIGINT NOT NULL DEFAULT 0,
    delta_reports_count BIGINT NOT NULL DEFAULT 0,
    updated_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_videos_creator ON videos(creator_id);
CREATE INDEX IF NOT EXISTS idx_videos_created ON videos(video_created_at);
CREATE INDEX IF NOT EXISTS idx_snapshots_created ON video_snapshots(created_at);
CREATE INDEX IF NOT EXISTS idx_snapshots_video ON video_snapshots(video_id);