CREATE TABLE IF NOT EXISTS `chat` (
  `no` int(11) NOT NULL AUTO_INCREMENT,
  `msg` text NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`no`),
  KEY `date` (`date`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;