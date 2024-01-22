-- MariaDB dump 10.19  Distrib 10.11.4-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: facemusix
-- ------------------------------------------------------
-- Server version	10.11.4-MariaDB-1~deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `amigos`
--

DROP TABLE IF EXISTS `amigos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `amigos` (
  `id_usuario` int(11) NOT NULL,
  `id_usuario_amigo` int(11) NOT NULL,
  PRIMARY KEY (`id_usuario`,`id_usuario_amigo`),
  KEY `fk_usuarioamigo2` (`id_usuario_amigo`),
  CONSTRAINT `fk_usuarioamigo` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `fk_usuarioamigo2` FOREIGN KEY (`id_usuario_amigo`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `amigos`
--

LOCK TABLES `amigos` WRITE;
/*!40000 ALTER TABLE `amigos` DISABLE KEYS */;
INSERT INTO `amigos` VALUES
(1,2),
(1,4),
(1,5),
(2,1),
(2,5),
(3,1),
(3,2),
(4,3),
(5,3);
/*!40000 ALTER TABLE `amigos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `canciones`
--

DROP TABLE IF EXISTS `canciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `canciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `título` varchar(100) DEFAULT NULL,
  `duración` time DEFAULT NULL,
  `album_id` int(11) DEFAULT NULL,
  `ratings_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_cancionalbum` (`album_id`),
  KEY `fk_cancionrating` (`ratings_id`),
  CONSTRAINT `fk_cancionalbum` FOREIGN KEY (`album_id`) REFERENCES `álbumes` (`id`),
  CONSTRAINT `fk_cancionrating` FOREIGN KEY (`ratings_id`) REFERENCES `ratings` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `canciones`
--

LOCK TABLES `canciones` WRITE;
/*!40000 ALTER TABLE `canciones` DISABLE KEYS */;
INSERT INTO `canciones` VALUES
(1,'Waka Waka','03:22:00',1,1),
(2,'Shape of You','03:54:00',2,2),
(3,'Formation','04:03:00',3,3),
(4,'Adventure of a Lifetime','04:24:00',4,4),
(5,'God s Plan','03:18:00',5,5),
(6,'Rolling in the Deep','03:49:00',6,6),
(7,'Love Story','03:56:00',7,7),
(8,'Hurricane','03:03:00',8,8),
(9,'Bad Guy','03:14:00',9,9),
(10,'Sorry','03:20:00',10,10);
/*!40000 ALTER TABLE `canciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cancionplaylist`
--

DROP TABLE IF EXISTS `cancionplaylist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cancionplaylist` (
  `playlist_id` int(11) NOT NULL,
  `cancion_id` int(11) NOT NULL,
  PRIMARY KEY (`playlist_id`,`cancion_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cancionplaylist`
--

LOCK TABLES `cancionplaylist` WRITE;
/*!40000 ALTER TABLE `cancionplaylist` DISABLE KEYS */;
INSERT INTO `cancionplaylist` VALUES
(1,1),
(1,2),
(1,3),
(1,4),
(1,5),
(2,6),
(2,7),
(2,8),
(3,9),
(3,10),
(4,1),
(4,2),
(5,3),
(5,4),
(5,5),
(6,6),
(6,7),
(6,8),
(6,9),
(7,10);
/*!40000 ALTER TABLE `cancionplaylist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlist`
--

DROP TABLE IF EXISTS `playlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlist`
--

LOCK TABLES `playlist` WRITE;
/*!40000 ALTER TABLE `playlist` DISABLE KEYS */;
INSERT INTO `playlist` VALUES
(1,'Playlist 1'),
(2,'Playlist 2'),
(3,'Playlist 3'),
(4,'Playlist 4'),
(5,'Playlist 5'),
(6,'Playlist 6'),
(7,'Playlist 7'),
(8,'Playlist 8'),
(9,'Playlist 9'),
(10,'Playlist 10');
/*!40000 ALTER TABLE `playlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratings`
--

DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ratings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(100) DEFAULT NULL,
  `comments` varchar(1000) DEFAULT NULL,
  `stars` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratings`
--

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
INSERT INTO `ratings` VALUES
(1,'1','¡Me encanta este himno mundial!',5),
(2,'2','Drake siempre entregando éxitos.',4),
(3,'3','Billie Eilish tiene un estilo único.',4),
(4,'4','Taylor Swift es la reina del country-pop.',5),
(5,'5','¡Justin Bieber sigue siendo el rey del pop!',3),
(6,'1','Beyoncé es puro fuego en esta canción.',5),
(7,'2','Kanye West siempre innovando en el rap.',4),
(8,'3','Ed Sheeran nunca decepciona.',4),
(9,'4','Adele con su voz poderosa.',5),
(10,'5','Coldplay lleva la música a otra dimensión.',4);
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url_avatar` varchar(1000) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `nombre_usuario` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `passwd` varchar(100) DEFAULT NULL,
  `artista` tinyint(1) DEFAULT NULL,
  `token` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES
(1,'https://avatar.com/user1.jpg','Juan','juanillo123','juan@email.com','82tc3j4tfmkjend834',0,NULL),
(2,'https://avatar.com/user2.jpg','Manuel','manolo72','manuel@email.com','klnf2j98j23id4mdi2o49',0,NULL),
(3,'https://avatar.com/user3.jpg','Marta','martitamichifu','marta@email.com','nf8hf24hdj43md28m4892345',1,NULL),
(4,'https://avatar.com/user4.jpg','Icía','ici21','icia@email.com','md904md8i34m9f85',0,NULL),
(5,'https://avatar.com/user5.jpg','Javier','javichuneymar','javier@email.com','m8934dm284dm2',0,NULL),
(6,NULL,NULL,'juanito123','juanito123@email.com@name=antoñete','pbkdf2_sha256$720000$vik7BZ0JL1GMPhZyHjHGiw$jsV0mcKDrFa680JcVDXm/ZCbmfwncBqtkqyw6+HDVi0=',NULL,NULL),
(7,NULL,'','juan','juanito123@email.com','pbkdf2_sha256$720000$cJVMtmvleTC59aiDvApNMe$PTsvWKhfnfU300uzQWsP6FJ5vPpBmlF+plqsV2YCsew=',NULL,NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `álbumes`
--

DROP TABLE IF EXISTS `álbumes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `álbumes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `título` varchar(100) DEFAULT NULL,
  `año` year(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `álbumes`
--

LOCK TABLES `álbumes` WRITE;
/*!40000 ALTER TABLE `álbumes` DISABLE KEYS */;
INSERT INTO `álbumes` VALUES
(1,'Sale el Sol',2010),
(2,'÷',2017),
(3,'Lemonade',2016),
(4,'A Head Full of Dreams',2015),
(5,'Scorpion',2018),
(6,'21',2011),
(7,'Fearless (Taylor’s Version)',2008),
(8,'Donda',2021),
(9,'Happier Than Ever',2021),
(10,'Purpose',2015);
/*!40000 ALTER TABLE `álbumes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-22 16:48:51
