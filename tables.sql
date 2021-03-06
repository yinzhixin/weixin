DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `open_id` varchar(255) NOT NULL COMMENT '用户微信openid',
  `input_content` varchar(255) NOT NULL COMMENT '用户输入内容',
  `req_ip` varchar(255) NOT NULL COMMENT '请求IP',
  `create_time` datetime,
  `last_time` datetime,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='用户表';

DROP TABLE IF EXISTS `user_movie_rel`;
CREATE TABLE `user_movie_rel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `open_id` varchar(255) NOT NULL,
  `movie_name` varchar(255),
  `create_time` datetime,
  PRIMARY KEY (`id`),
  INDEX (`open_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='用户电影关系表';

DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_name` VARCHAR(255) NOT NULL COMMENT '电影名称',
  `movie_desc` VARCHAR(255) NOT NULL COMMENT '电影描述',
  `movie_image` VARCHAR(255) NOT NULL COMMENT '电影图片',
  `movie_link` VARCHAR(255) NOT NULL COMMENT '电影链接',
  `create_time` DATETIME,
  `update_time` DATETIME,
  `albumid` int(11),
  PRIMARY KEY (`id`)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='电影信息表';
