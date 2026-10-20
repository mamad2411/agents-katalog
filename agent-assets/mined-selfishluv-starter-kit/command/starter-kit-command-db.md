# Supabase 마이그레이션/쿼리 가이드
$ARGUMENTS로 원하는 쿼리 또는 테이블 변경사항을 받아 Supabase SQL 마이그레이션 초안을 생성합니다.
RLS(Row Level Security) 정책 템플릿도 함께 제공하며,
새 테이블 추가 또는 쿼리 최적화가 필요할 때 사용합니다.
예: /db add-comments-table