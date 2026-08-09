-- ============================================================
-- Flyway Migration: V1__create_sys_user_table.sql
-- Description : 创建系统用户表 (sys_user)
-- Author      : auto-generated
-- Date        : 2026-08-09
-- ============================================================

-- 如果表已存在则先删除（仅开发环境使用，生产环境请移除）
-- DROP TABLE IF EXISTS `sys_user`;

CREATE TABLE `sys_user` (
    `id`         BIGINT       UNSIGNED NOT NULL AUTO_INCREMENT  COMMENT '用户ID（主键）',
    `username`   VARCHAR(64)  NOT NULL                          COMMENT '用户名',
    `email`      VARCHAR(128) NOT NULL DEFAULT ''               COMMENT '邮箱',
    `status`     TINYINT      NOT NULL DEFAULT 1                COMMENT '状态：1=正常，2=禁用',
    `created_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统用户表';

-- ============================================================
-- 初始化测试数据（开发环境使用）
-- ============================================================
INSERT INTO `sys_user` (`username`, `email`, `status`) VALUES
    ('admin',    'admin@example.com',    1),
    ('zhangsan', 'zhangsan@example.com', 1),
    ('lisi',     'lisi@example.com',     1),
    ('wangwu',   'wangwu@example.com',   2),
    ('zhaoliu',  'zhaoliu@example.com',  1);
