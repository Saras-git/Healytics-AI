-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 20, 2024 at 05:39 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `organ_donation`
--

-- --------------------------------------------------------

--
-- Table structure for table `od_agreement`
--

CREATE TABLE `od_agreement` (
  `id` int(11) NOT NULL,
  `donor_id` varchar(20) NOT NULL,
  `name1` varchar(20) NOT NULL,
  `proof1` varchar(50) NOT NULL,
  `sign1` varchar(50) NOT NULL,
  `name2` varchar(20) NOT NULL,
  `proof2` varchar(50) NOT NULL,
  `sign2` varchar(50) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `od_agreement`
--

INSERT INTO `od_agreement` (`id`, `donor_id`, `name1`, `proof1`, `sign1`, `name2`, `proof2`, `sign2`, `create_date`, `dtime`) VALUES
(1, 'DN230001', 'Raji', 'P11d1.jpg', 'S1102_0119019.PNG', 'Kannan', 'P21d2.jpg', 'S2110_018.png', '10-02-2023', '2024-11-20 21:52:35');

-- --------------------------------------------------------

--
-- Table structure for table `od_donor`
--

CREATE TABLE `od_donor` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `aadhar` varchar(20) NOT NULL,
  `pancard` varchar(20) NOT NULL,
  `guardian` varchar(20) NOT NULL,
  `mobile2` bigint(20) NOT NULL,
  `blood_grp` varchar(10) NOT NULL,
  `organ` varchar(100) NOT NULL,
  `photo` varchar(100) NOT NULL,
  `donor_id` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `hospital` varchar(20) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `trans_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `od_donor`
--

INSERT INTO `od_donor` (`id`, `name`, `gender`, `dob`, `address`, `city`, `mobile`, `email`, `aadhar`, `pancard`, `guardian`, `mobile2`, `blood_grp`, `organ`, `photo`, `donor_id`, `pass`, `create_date`, `hospital`, `dtime`, `trans_st`) VALUES
(1, 'Ravi', 'Male', '1985-02-17', 'DG Nagar', 'Salem', 7894545121, 'ravi1785@gmail.com', '246813571123', '2354585517', 'Kannan', 8889574168, 'A+ve', 'Heart,Kidneys,Pancreas', 'D1face27.jpg', 'DN230001', '123456', '10-02-2023', 'apollo', '2024-11-20 14:05:50', 0),
(2, 'Rajan', 'Male', '1974-08-22', 'MK Road', 'Madurai', 9054774696, 'rajan@gmail.com', '678967896789', '2094254832', 'Latha', 7365685427, 'B+ve', 'Heart,Kidneys,Pancreas', 'D2face18.jpg', 'DN230002', '123456', '20-11-2024', 'apollo', '2024-11-20 16:12:57', 0);

-- --------------------------------------------------------

--
-- Table structure for table `od_hospital`
--

CREATE TABLE `od_hospital` (
  `id` int(11) NOT NULL,
  `hospital` varchar(30) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `od_hospital`
--

INSERT INTO `od_hospital` (`id`, `hospital`, `address`, `city`, `mobile`, `email`, `uname`, `pass`, `create_date`, `status`, `dtime`) VALUES
(1, 'Apollo', '57, MG Nagar', 'Trichy', 9054621096, 'apollo@gmail.com', 'apollo', '123456', '20-11-2024', 1, '2024-11-20 12:38:01');

-- --------------------------------------------------------

--
-- Table structure for table `od_login`
--

CREATE TABLE `od_login` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `utype` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `od_login`
--

INSERT INTO `od_login` (`username`, `password`, `utype`) VALUES
('admin', 'admin', 'admin'),
('opo', '123456', 'opo');

-- --------------------------------------------------------

--
-- Table structure for table `od_patient`
--

CREATE TABLE `od_patient` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `aadhar` varchar(20) NOT NULL,
  `guardian` varchar(20) NOT NULL,
  `mobile2` bigint(20) NOT NULL,
  `blood_grp` varchar(10) NOT NULL,
  `patient_id` varchar(20) NOT NULL,
  `create_date` varchar(20) NOT NULL,
  `hospital` varchar(20) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `status` int(11) NOT NULL,
  `organ_required` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `od_patient`
--

INSERT INTO `od_patient` (`id`, `name`, `gender`, `dob`, `address`, `city`, `mobile`, `email`, `aadhar`, `guardian`, `mobile2`, `blood_grp`, `patient_id`, `create_date`, `hospital`, `dtime`, `status`, `organ_required`) VALUES
(1, 'Varun', 'Male', '1985-05-25', 'FF Nagar', 'Erode', 8845576994, 'varun@gmail.com', '255678894331', 'Suresh', 7388549662, 'B+ve', 'PT0001', '20-11-2024', 'apollo', '2024-11-20 16:41:15', 0, ''),
(2, 'Rajan', 'Male', '1974-08-22', 'MK Road', 'Madurai', 9054774696, 'rajan@gmail.com', '678967896789', 'Latha', 7365685427, 'B+ve', 'PT0002', '20-11-2024', 'apollo', '2024-11-20 08:12:37', 2, '');

-- --------------------------------------------------------

--
-- Table structure for table `od_request`
--

CREATE TABLE `od_request` (
  `id` int(11) NOT NULL,
  `pat_id` varchar(20) NOT NULL,
  `hospital` varchar(20) NOT NULL,
  `organ` varchar(20) NOT NULL,
  `status` int(11) NOT NULL,
  `donor_id` varchar(20) NOT NULL,
  `trans_date` varchar(20) NOT NULL,
  `dtime` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `od_request`
--

INSERT INTO `od_request` (`id`, `pat_id`, `hospital`, `organ`, `status`, `donor_id`, `trans_date`, `dtime`) VALUES
(1, 'PT0001', 'apollo', 'Heart', 0, '', '', '2024-11-20 17:43:30'),
(2, 'PT0001', 'apollo', 'Heart', 0, '', '', '2024-11-20 06:14:26');
