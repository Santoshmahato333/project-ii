# FilmyFix Movie Recommendation System - Database Schema Design

## 📋 Overview

The FilmyFix database schema is designed for a comprehensive movie recommendation system that combines user-generated content with external movie data from TMDB API. The schema supports user authentication, movie reviews and ratings, recommendation tracking, and analytics.

## 🗂️ Database Structure

### **Database Type**: SQLite
### **Total Tables**: 7
### **Total Indexes**: 20+
### **Views**: 3
### **Triggers**: 4

---

## 📊 Core Tables

### 1. **users** - User Management
**Purpose**: Central user account management and authentication

**Key Features**:
- Unique username and email constraints
- Password hashing support
- Account status tracking
- Login history
- Data validation (username length, email format)

**Primary Relationships**:
- One-to-Many with `reviews`
- One-to-Many with `ratings`
- One-to-Many with `user_sessions`
- One-to-Many with `recommendation_history`

### 2. **movies** - Movie Data Repository
**Purpose**: Comprehensive movie information storage

**Key Features**:
- Complete TMDB movie metadata
- Financial data (budget, revenue)
- Popularity metrics and ratings
- Genre information (JSON format)
- Poster and backdrop image paths
- Data validation for ratings and metrics

**Primary Relationships**:
- One-to-Many with `movie_genres`
- One-to-Many with `reviews`
- One-to-Many with `ratings`
- Many-to-Many with `recommendation_history`

### 3. **reviews** - User-Generated Reviews
**Purpose**: Detailed user reviews with text content and ratings

**Key Features**:
- Text content with minimum length requirement
- Rating system (1-5 stars)
- One review per user per movie constraint
- Timestamp tracking
- Foreign key relationships with cascade delete

**Primary Relationships**:
- Many-to-One with `users`
- Many-to-One with `movies`

### 4. **ratings** - Simple User Ratings
**Purpose**: Quick numeric ratings separate from reviews

**Key Features**:
- Simple 1-5 star rating system
- One rating per user per movie constraint
- Separate from detailed reviews
- Efficient for quick rating operations

**Primary Relationships**:
- Many-to-One with `users`
- Many-to-One with `movies`

### 5. **user_sessions** - Session Management
**Purpose**: User session tracking and authentication

**Key Features**:
- Secure session token storage
- Automatic expiration handling
- User activity tracking
- Session cleanup triggers

**Primary Relationships**:
- Many-to-One with `users`

### 6. **recommendation_history** - Recommendation Analytics
**Purpose**: Track recommendation requests and similarity scores

**Key Features**:
- Stores recommendation requests
- Tracks similarity scores
- Enables recommendation analytics
- Supports recommendation improvement

**Primary Relationships**:
- Many-to-One with `users`
- Many-to-One with `movies` (source)
- Many-to-One with `movies` (recommended)

### 7. **movie_genres** - Normalized Genre Data
**Purpose**: Efficient genre-based queries and filtering

**Key Features**:
- Normalized genre relationships
- Many-to-many movie-genre support
- Efficient genre-based queries
- Supports genre analytics

**Primary Relationships**:
- Many-to-One with `movies`

---

## 🔗 Relationships & Constraints

### **Primary Key Constraints**
- All tables have auto-incrementing primary keys
- Ensures unique identification of records

### **Foreign Key Constraints**
- All foreign keys have CASCADE DELETE
- Maintains referential integrity
- Automatic cleanup of related data

### **Unique Constraints**
- `users.username` - Unique usernames
- `users.email` - Unique email addresses
- `reviews(user_id, movie_id)` - One review per user per movie
- `ratings(user_id, movie_id)` - One rating per user per movie
- `user_sessions.session_token` - Unique session tokens
- `movie_genres(movie_id, genre_id)` - Unique genre per movie

### **Check Constraints**
- Rating values: 1.0 to 5.0
- Review content: Minimum 10 characters
- Username: Minimum 3 characters
- Email: Valid email format
- Movie metrics: Non-negative values
- Similarity scores: 0.0 to 1.0

---

## ⚡ Performance Optimizations

### **Strategic Indexing**
- **User queries**: username, email, active status
- **Movie queries**: title, release date, popularity, ratings
- **Review/Rating queries**: user_id, movie_id, ratings, timestamps
- **Composite indexes**: user-movie combinations for unique constraints
- **Session queries**: tokens, expiration dates
- **Analytics queries**: recommendation history, user activity

### **Views for Complex Queries**
1. **movie_ratings_summary**: Combined TMDB and user ratings
2. **user_activity_summary**: User engagement metrics
3. **popular_movies**: Trending movies by user activity

### **Triggers for Data Integrity**
- Automatic timestamp updates
- Session cleanup
- Data consistency maintenance

---

## 📈 Analytics & Reporting

### **Available Metrics**
- User engagement statistics
- Movie popularity rankings
- Rating distribution analysis
- Recommendation effectiveness
- Genre popularity trends
- User activity patterns

### **Sample Queries**
```sql
-- Get top-rated movies
SELECT * FROM popular_movies LIMIT 10;

-- User activity summary
SELECT * FROM user_activity_summary WHERE movies_reviewed > 5;

-- Movie ratings comparison
SELECT * FROM movie_ratings_summary WHERE avg_user_rating > 4.0;
```

---

## 🔒 Security Features

### **Authentication Security**
- Password hashing (bcrypt recommended)
- Secure session token generation
- Session expiration management
- Account status tracking

### **Data Protection**
- Input validation at database level
- SQL injection prevention through constraints
- Foreign key integrity enforcement
- Unique constraint protection

### **Privacy Considerations**
- User data isolation
- Session data cleanup
- Audit trail through timestamps

---

## 🛠️ Maintenance & Operations

### **Regular Maintenance Tasks**
- Session cleanup (expired sessions)
- Statistics updates (average ratings)
- Data archiving (old recommendation history)
- Index optimization (VACUUM and ANALYZE)

### **Backup Strategy**
- Regular database backups
- Incremental backup support
- Point-in-time recovery capability

### **Monitoring Queries**
```sql
-- Check database size
SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size();

-- Monitor active sessions
SELECT COUNT(*) FROM user_sessions WHERE is_active = 1;

-- Check data integrity
SELECT COUNT(*) FROM reviews r LEFT JOIN users u ON r.user_id = u.id WHERE u.id IS NULL;
```

---

## 🚀 Scalability Considerations

### **Current Design Benefits**
- Efficient indexing strategy
- Normalized data structure
- Optimized query patterns
- Minimal redundancy

### **Future Scalability Options**
- Partitioning for large datasets
- Read replicas for analytics
- Caching layer for popular queries
- Horizontal scaling considerations

---

## 📋 Implementation Notes

### **Database Creation**
```bash
# Create database
sqlite3 filmyfix.db < filmyfix_database_schema.sql

# Verify tables
.tables

# Check indexes
SELECT name FROM sqlite_master WHERE type='index';
```

### **Sample Data Population**
- Sample users for testing
- Popular movies from TMDB
- Sample reviews and ratings
- Realistic data relationships

### **Integration with Application**
- SQLAlchemy ORM models already defined
- Flask-Login integration ready
- Session management implemented
- Recommendation engine compatible

---

## 🎯 Key Advantages

1. **Comprehensive Coverage**: Handles all aspects of movie recommendation system
2. **Performance Optimized**: Strategic indexing and query optimization
3. **Data Integrity**: Robust constraints and validation
4. **Analytics Ready**: Built-in views and reporting capabilities
5. **Security Focused**: Authentication and session management
6. **Scalable Design**: Supports growth and future enhancements
7. **Maintenance Friendly**: Automated cleanup and optimization

This database schema provides a solid foundation for your FilmyFix movie recommendation system and can scale with your application's growth! 