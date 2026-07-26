CREATE SCHEMA IF NOT EXISTS core;

SET search_path TO core;

DROP TABLE IF EXISTS core.course_skills;
DROP TABLE IF EXISTS core.trainer_skills;
DROP TABLE IF EXISTS core.courses;
DROP TABLE IF EXISTS core.skills;
DROP TABLE IF EXISTS core.trainers;

CREATE TABLE core.trainers (
    trainer_id BIGSERIAL PRIMARY KEY,
    trainer_code VARCHAR(50) NOT NULL UNIQUE,
    trainer_name VARCHAR(200) NOT NULL,
    email VARCHAR(255),
    experience_years INT,
    primary_location VARCHAR(100),
    availability_percentage NUMERIC(5, 2),
    status VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE core.skills (
    skill_id BIGSERIAL PRIMARY KEY,
    skill_code VARCHAR(50) NOT NULL UNIQUE,
    skill_name VARCHAR(200) NOT NULL,
    skill_category VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE core.courses (
    course_id BIGSERIAL PRIMARY KEY,
    course_code VARCHAR(50) NOT NULL UNIQUE,
    course_name VARCHAR(200),
    duration_days NUMERIC(5, 2),
    level VARCHAR(50),
    technology_area VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE core.trainer_skills (
    trainer_skill_id BIGSERIAL PRIMARY KEY,
    trainer_id BIGINT NOT NULL,
    skill_id BIGINT NOT NULL,
    proficiency VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_trainer_skills_trainer_skill UNIQUE (trainer_id, skill_id),
    CONSTRAINT fk_trainer_skills_trainer
        FOREIGN KEY (trainer_id) REFERENCES core.trainers (trainer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_trainer_skills_skill
        FOREIGN KEY (skill_id) REFERENCES core.skills (skill_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE core.course_skills (
    course_skill_id BIGSERIAL PRIMARY KEY,
    course_id BIGINT NOT NULL,
    skill_id BIGINT NOT NULL,
    importance VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_course_skills_course_skill UNIQUE (course_id, skill_id),
    CONSTRAINT fk_course_skills_course
        FOREIGN KEY (course_id) REFERENCES core.courses (course_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_course_skills_skill
        FOREIGN KEY (skill_id) REFERENCES core.skills (skill_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_trainers_trainer_code ON core.trainers (trainer_code);
CREATE INDEX idx_skills_skill_code ON core.skills (skill_code);
CREATE INDEX idx_courses_course_code ON core.courses (course_code);

CREATE INDEX idx_trainer_skills_trainer_id ON core.trainer_skills (trainer_id);
CREATE INDEX idx_trainer_skills_skill_id ON core.trainer_skills (skill_id);
CREATE INDEX idx_course_skills_course_id ON core.course_skills (course_id);
CREATE INDEX idx_course_skills_skill_id ON core.course_skills (skill_id);

CREATE OR REPLACE FUNCTION core.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_trainers_set_updated_at
BEFORE UPDATE ON core.trainers
FOR EACH ROW
EXECUTE FUNCTION core.set_updated_at();

CREATE TRIGGER trg_skills_set_updated_at
BEFORE UPDATE ON core.skills
FOR EACH ROW
EXECUTE FUNCTION core.set_updated_at();

CREATE TRIGGER trg_courses_set_updated_at
BEFORE UPDATE ON core.courses
FOR EACH ROW
EXECUTE FUNCTION core.set_updated_at();

CREATE TRIGGER trg_trainer_skills_set_updated_at
BEFORE UPDATE ON core.trainer_skills
FOR EACH ROW
EXECUTE FUNCTION core.set_updated_at();

CREATE TRIGGER trg_course_skills_set_updated_at
BEFORE UPDATE ON core.course_skills
FOR EACH ROW
EXECUTE FUNCTION core.set_updated_at();
