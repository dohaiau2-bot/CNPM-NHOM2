-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 01, 2025 at 03:11 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library`
--

-- --------------------------------------------------------

--
-- Table structure for table `audit_log`
--

CREATE TABLE `audit_log` (
  `id` bigint(20) NOT NULL,
  `actor` varchar(150) DEFAULT NULL,
  `action` varchar(150) DEFAULT NULL,
  `object_type` varchar(100) DEFAULT NULL,
  `object_id` varchar(100) DEFAULT NULL,
  `details` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `authors`
--

CREATE TABLE `authors` (
  `id` int(11) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `bio` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `authors`
--

INSERT INTO `authors` (`id`, `full_name`, `bio`, `created_at`) VALUES
(1, 'Nguyễn Nhật Ánh', 'Nhà văn nổi tiếng', '2025-12-01 14:10:57'),
(2, 'Trần Minh Tân', 'Chuyên gia CNTT', '2025-12-01 14:10:57'),
(3, 'Stephen Hawking', 'Nhà khoa học vũ trụ', '2025-12-01 14:10:57');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `code` varchar(50) NOT NULL,
  `title` varchar(500) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `publisher_id` int(11) DEFAULT NULL,
  `publication_year` smallint(6) DEFAULT NULL,
  `isbn` varchar(30) DEFAULT NULL,
  `total_copies` int(11) NOT NULL DEFAULT 0,
  `available_copies` int(11) NOT NULL DEFAULT 0,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `code`, `title`, `category_id`, `publisher_id`, `publication_year`, `isbn`, `total_copies`, `available_copies`, `description`, `created_at`, `updated_at`) VALUES
(1, 'BK001', 'Lập trình C cơ bản', 1, 2, 2020, 'ISBN001', 5, 5, NULL, '2025-12-01 14:10:57', '2025-12-01 14:10:57'),
(2, 'BK002', 'Mắt biếc', 3, 1, 2009, 'ISBN002', 3, 3, NULL, '2025-12-01 14:10:57', '2025-12-01 14:10:57'),
(3, 'BK003', 'Lược sử thời gian', 2, 3, 1988, 'ISBN003', 4, 4, NULL, '2025-12-01 14:10:57', '2025-12-01 14:10:57');

-- --------------------------------------------------------

--
-- Table structure for table `book_authors`
--

CREATE TABLE `book_authors` (
  `book_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `book_authors`
--

INSERT INTO `book_authors` (`book_id`, `author_id`) VALUES
(1, 2),
(2, 1),
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `borrows`
--

CREATE TABLE `borrows` (
  `id` bigint(20) NOT NULL,
  `borrow_code` varchar(50) NOT NULL,
  `reader_id` bigint(20) NOT NULL,
  `staff` varchar(150) DEFAULT NULL,
  `borrow_date` datetime NOT NULL DEFAULT current_timestamp(),
  `due_date` datetime NOT NULL,
  `returned` tinyint(1) DEFAULT 0,
  `return_date` datetime DEFAULT NULL,
  `note` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `borrows`
--

INSERT INTO `borrows` (`id`, `borrow_code`, `reader_id`, `staff`, `borrow_date`, `due_date`, `returned`, `return_date`, `note`, `created_at`) VALUES
(1, 'BR001', 1, 'Thủ thư Lan', '2025-12-01 21:10:57', '2025-12-08 21:10:57', 0, NULL, NULL, '2025-12-01 14:10:57');

-- --------------------------------------------------------

--
-- Table structure for table `borrow_items`
--

CREATE TABLE `borrow_items` (
  `id` bigint(20) NOT NULL,
  `borrow_id` bigint(20) NOT NULL,
  `copy_id` bigint(20) DEFAULT NULL,
  `book_id` int(11) NOT NULL,
  `status` enum('borrowed','returned','lost','damaged') DEFAULT 'borrowed',
  `due_date` datetime NOT NULL,
  `returned_at` datetime DEFAULT NULL,
  `late_days` int(11) DEFAULT 0,
  `late_fee` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `borrow_items`
--

INSERT INTO `borrow_items` (`id`, `borrow_id`, `copy_id`, `book_id`, `status`, `due_date`, `returned_at`, `late_days`, `late_fee`) VALUES
(1, 1, 1, 1, 'borrowed', '2025-12-08 21:10:57', NULL, 0, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `name`, `description`, `created_at`) VALUES
(1, 'Lập trình', 'Sách dạy lập trình', '2025-12-01 14:10:57'),
(2, 'Khoa học', 'Sách khoa học', '2025-12-01 14:10:57'),
(3, 'Văn học', 'Tác phẩm văn học', '2025-12-01 14:10:57'),
(4, 'Kinh tế', 'Sách kinh tế - tài chính', '2025-12-01 14:10:57');

-- --------------------------------------------------------

--
-- Table structure for table `copies`
--

CREATE TABLE `copies` (
  `id` bigint(20) NOT NULL,
  `book_id` int(11) NOT NULL,
  `barcode` varchar(100) DEFAULT NULL,
  `acquisition_date` date DEFAULT NULL,
  `status` enum('available','borrowed','reserved','lost','damaged') NOT NULL DEFAULT 'available',
  `location` varchar(200) DEFAULT NULL,
  `note` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `copies`
--

INSERT INTO `copies` (`id`, `book_id`, `barcode`, `acquisition_date`, `status`, `location`, `note`) VALUES
(1, 1, 'CPY001-A', '2023-01-10', 'available', NULL, NULL),
(2, 1, 'CPY001-B', '2023-01-10', 'available', NULL, NULL),
(3, 2, 'CPY002-A', '2023-02-12', 'available', NULL, NULL),
(4, 3, 'CPY003-A', '2023-03-05', 'available', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `fines`
--

CREATE TABLE `fines` (
  `id` bigint(20) NOT NULL,
  `reader_id` bigint(20) NOT NULL,
  `borrow_item_id` bigint(20) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `reason` varchar(300) DEFAULT NULL,
  `paid` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `paid_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `fines`
--

INSERT INTO `fines` (`id`, `reader_id`, `borrow_item_id`, `amount`, `reason`, `paid`, `created_at`, `paid_at`) VALUES
(1, 1, 1, 5000.00, 'Trả sách trễ 1 ngày', 0, '2025-12-01 14:10:57', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id` bigint(20) NOT NULL,
  `reader_id` bigint(20) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `sent_at` datetime DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `reader_id`, `title`, `message`, `sent_at`, `is_read`) VALUES
(1, 1, 'Nhắc nhở trả sách', 'Bạn đang trễ hạn trả sách BK001', '2025-12-01 21:10:57', 0);

-- --------------------------------------------------------

--
-- Table structure for table `publishers`
--

CREATE TABLE `publishers` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `address` text DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `publishers`
--

INSERT INTO `publishers` (`id`, `name`, `address`, `contact`, `created_at`) VALUES
(1, 'NXB Trẻ', 'TP.HCM', '0123 456 789', '2025-12-01 14:10:57'),
(2, 'NXB Giáo dục', 'Hà Nội', '0987 654 321', '2025-12-01 14:10:57'),
(3, 'NXB Khoa học', 'Đà Nẵng', '0236 111 222', '2025-12-01 14:10:57');

-- --------------------------------------------------------

--
-- Table structure for table `readers`
--

CREATE TABLE `readers` (
  `id` bigint(20) NOT NULL,
  `reader_code` varchar(50) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `type` enum('student','staff','other') DEFAULT 'student',
  `email` varchar(200) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `is_blocked` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `readers`
--

INSERT INTO `readers` (`id`, `reader_code`, `full_name`, `type`, `email`, `phone`, `address`, `is_blocked`, `created_at`, `updated_at`) VALUES
(1, 'RD001', 'Nguyễn Văn A', 'student', 'a@gmail.com', NULL, NULL, 0, '2025-12-01 14:10:57', '2025-12-01 14:10:57'),
(2, 'RD002', 'Trần Thị B', 'student', 'b@gmail.com', NULL, NULL, 0, '2025-12-01 14:10:57', '2025-12-01 14:10:57');

-- --------------------------------------------------------

--
-- Table structure for table `violations`
--

CREATE TABLE `violations` (
  `id` bigint(20) NOT NULL,
  `reader_id` bigint(20) NOT NULL,
  `type` enum('late_return','lost_book','damaged_book','other') NOT NULL,
  `description` text DEFAULT NULL,
  `penalty_amount` decimal(10,2) DEFAULT 0.00,
  `resolved` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `violations`
--

INSERT INTO `violations` (`id`, `reader_id`, `type`, `description`, `penalty_amount`, `resolved`, `created_at`) VALUES
(1, 1, 'late_return', 'Trả sách trễ hạn', 5000.00, 0, '2025-12-01 14:10:57');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `audit_log`
--
ALTER TABLE `audit_log`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `authors`
--
ALTER TABLE `authors`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ux_authors_name` (`full_name`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `publisher_id` (`publisher_id`);

--
-- Indexes for table `book_authors`
--
ALTER TABLE `book_authors`
  ADD PRIMARY KEY (`book_id`,`author_id`),
  ADD KEY `author_id` (`author_id`);

--
-- Indexes for table `borrows`
--
ALTER TABLE `borrows`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `borrow_code` (`borrow_code`),
  ADD KEY `reader_id` (`reader_id`);

--
-- Indexes for table `borrow_items`
--
ALTER TABLE `borrow_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `borrow_id` (`borrow_id`),
  ADD KEY `copy_id` (`copy_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `copies`
--
ALTER TABLE `copies`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `barcode` (`barcode`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `fines`
--
ALTER TABLE `fines`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reader_id` (`reader_id`),
  ADD KEY `borrow_item_id` (`borrow_item_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reader_id` (`reader_id`);

--
-- Indexes for table `publishers`
--
ALTER TABLE `publishers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `readers`
--
ALTER TABLE `readers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reader_code` (`reader_code`);

--
-- Indexes for table `violations`
--
ALTER TABLE `violations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reader_id` (`reader_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `audit_log`
--
ALTER TABLE `audit_log`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `authors`
--
ALTER TABLE `authors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `borrows`
--
ALTER TABLE `borrows`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `borrow_items`
--
ALTER TABLE `borrow_items`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `copies`
--
ALTER TABLE `copies`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `fines`
--
ALTER TABLE `fines`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `publishers`
--
ALTER TABLE `publishers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `readers`
--
ALTER TABLE `readers`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `violations`
--
ALTER TABLE `violations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `books_ibfk_2` FOREIGN KEY (`publisher_id`) REFERENCES `publishers` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `book_authors`
--
ALTER TABLE `book_authors`
  ADD CONSTRAINT `book_authors_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `book_authors_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `borrows`
--
ALTER TABLE `borrows`
  ADD CONSTRAINT `borrows_ibfk_1` FOREIGN KEY (`reader_id`) REFERENCES `readers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `borrow_items`
--
ALTER TABLE `borrow_items`
  ADD CONSTRAINT `borrow_items_ibfk_1` FOREIGN KEY (`borrow_id`) REFERENCES `borrows` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `borrow_items_ibfk_2` FOREIGN KEY (`copy_id`) REFERENCES `copies` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `borrow_items_ibfk_3` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `copies`
--
ALTER TABLE `copies`
  ADD CONSTRAINT `copies_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `fines`
--
ALTER TABLE `fines`
  ADD CONSTRAINT `fines_ibfk_1` FOREIGN KEY (`reader_id`) REFERENCES `readers` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fines_ibfk_2` FOREIGN KEY (`borrow_item_id`) REFERENCES `borrow_items` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`reader_id`) REFERENCES `readers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `violations`
--
ALTER TABLE `violations`
  ADD CONSTRAINT `violations_ibfk_1` FOREIGN KEY (`reader_id`) REFERENCES `readers` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
