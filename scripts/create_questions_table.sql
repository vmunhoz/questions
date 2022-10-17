CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` text NOT NULL,
  `author` varchar(128) DEFAULT NULL,
  `answered` tinyint NOT NULL DEFAULT '0',
  `authorized` tinyint NOT NULL DEFAULT '0',
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
