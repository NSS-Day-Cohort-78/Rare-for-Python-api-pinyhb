-- RUN THIS BLOCK TO DELETE ALL
DELETE FROM Users;
DELETE FROM DemotionQueue;
DELETE FROM Subscriptions;
DELETE FROM Posts;
DELETE FROM Comments;
DELETE FROM Reactions;
DELETE FROM PostReactions;
DELETE FROM Tags;
DELETE FROM PostTags;
DELETE FROM Categories;

DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS DemotionQueue;
DROP TABLE IF EXISTS Subscriptions;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Reactions;
DROP TABLE IF EXISTS PostReactions;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS PostTags;
DROP TABLE IF EXISTS Categories;


-- END BLOCK

-- Run this to seed DB

CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  "creation_date" date,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

-- Seed Users
INSERT INTO "Users" (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active) VALUES
('John', 'Doe', 'john.doe@example.com', 'Software developer passionate about web technologies', 'johndoe', 'password123', 'https://i.pravatar.cc/150?img=1', '2024-01-15', 1),
('Jane', 'Smith', 'jane.smith@example.com', 'Tech writer and blogger', 'janesmith', 'password123', 'https://i.pravatar.cc/150?img=2', '2024-01-20', 1),
('Mike', 'Johnson', 'mike.j@example.com', 'Full-stack developer and open source contributor', 'mikej', 'password123', 'https://i.pravatar.cc/150?img=3', '2024-02-01', 1),
('Sarah', 'Williams', 'sarah.w@example.com', 'UX designer who loves writing about design', 'sarahw', 'password123', 'https://i.pravatar.cc/150?img=4', '2024-02-10', 1),
('Admin', 'User', 'admin@example.com', 'Site administrator', 'admin', 'admin123', 'https://i.pravatar.cc/150?img=5', '2024-01-01', 1);

-- Seed Categories
INSERT INTO "Categories" (label) VALUES
('Technology'),
('Design'),
('Programming'),
('Lifestyle'),
('Tutorial'),
('News');

-- Seed Tags
INSERT INTO "Tags" (label) VALUES
('JavaScript'),
('Python'),
('Web Development'),
('Mobile'),
('AI/ML'),
('DevOps'),
('UI/UX'),
('Career'),
('Beginner'),
('Advanced');

-- Seed Reactions
INSERT INTO "Reactions" (label, image_url) VALUES
('Like', '👍'),
('Love', '❤️'),
('Insightful', '💡'),
('Funny', '😄'),
('Celebrate', '🎉');

-- Seed Posts
INSERT INTO "Posts" (user_id, category_id, title, publication_date, image_url, content, approved) VALUES
(1, 1, 'Getting Started with React Hooks', '2024-03-01', 'https://picsum.photos/800/400?random=1', 'React Hooks revolutionized how we write React components. In this post, we explore useState and useEffect...', 1),
(2, 3, 'Python Best Practices for 2024', '2024-03-05', 'https://picsum.photos/800/400?random=2', 'Writing clean, maintainable Python code is essential. Here are the top practices every developer should follow...', 1),
(3, 5, 'Building Your First REST API', '2024-03-10', 'https://picsum.photos/800/400?random=3', 'A step-by-step guide to creating a REST API from scratch using Node.js and Express...', 1),
(4, 2, 'The Psychology of Color in Web Design', '2024-03-12', 'https://picsum.photos/800/400?random=4', 'Colors evoke emotions and influence user behavior. Learn how to choose the right palette for your website...', 1),
(1, 1, 'Introduction to Machine Learning', '2024-03-15', 'https://picsum.photos/800/400?random=5', 'Machine learning is transforming industries. This beginner-friendly guide covers the fundamentals...', 1),
(3, 6, 'Tech Industry Trends 2024', '2024-03-18', 'https://picsum.photos/800/400?random=6', 'The tech landscape is evolving rapidly. Here are the key trends shaping the industry this year...', 0);

-- Seed Subscriptions
INSERT INTO "Subscriptions" (follower_id, author_id, created_on) VALUES
(2, 1, '2024-02-15'),
(3, 1, '2024-02-20'),
(4, 1, '2024-02-25'),
(1, 2, '2024-02-18'),
(3, 2, '2024-03-01'),
(1, 4, '2024-03-05'),
(2, 3, '2024-03-08');

-- Seed Comments
INSERT INTO "Comments" (post_id, author_id, content, creation_date) VALUES
(1, 2, 'Great explanation! This really helped me understand hooks better.', '2024-01-15'),
(1, 3, 'Thanks for sharing. Do you have any tips for custom hooks?', '2024-01-16'),
(2, 1, 'Excellent post! The type hints section was particularly useful.', '2024-01-20'),
(3, 4, 'Very comprehensive tutorial. Looking forward to trying this out!', '2024-02-05'),
(4, 1, 'Fascinating read! Never thought about color psychology this deeply.', '2024-02-12'),
(1, 4, 'Bookmarked for future reference. Clear and concise!', '2024-01-17');

-- Seed PostTags
INSERT INTO "PostTags" (post_id, tag_id) VALUES
(1, 1), (1, 3), (1, 9),
(2, 2), (2, 10),
(3, 1), (3, 3), (3, 5), (3, 9),
(4, 7), (4, 3),
(5, 5), (5, 9),
(6, 1), (6, 2), (6, 8);

-- Seed PostReactions
INSERT INTO "PostReactions" (user_id, reaction_id, post_id) VALUES
(2, 1, 1), (3, 2, 1), (4, 3, 1),
(1, 1, 2), (3, 1, 2),
(4, 2, 3), (2, 3, 3),
(1, 2, 4), (3, 1, 4),
(2, 3, 5), (4, 5, 5);

-- Seed DemotionQueue (example of pending admin actions)
INSERT INTO "DemotionQueue" (action, admin_id, approver_one_id) VALUES
('demote_user_3', 5, 1),
('remove_post_6', 5, 2);

DELETE FROM Subscriptions WHERE id = 9