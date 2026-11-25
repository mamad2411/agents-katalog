#!/usr/bin/env bash
# Uji asap auth BFF (cookie httpOnly, CSRF, rate limit, anti-enumerasi).
# Pakai: auth-smoke.sh http://localhost:3100   (butuh FE + backend hidup; membuat 1 akun uji)
B=${1:-http://localhost:3100}; H=(-H "Origin: $B" -H "Content-Type: application/json")
E="smoke.$(date +%s)@example.com"; P='Kuat-Sandi-2026!'; CJ=$(mktemp); FAIL=0
t(){ if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (dapat '$2', harap '$3')"; FAIL=1; fi; }
post(){ curl -s -o /dev/null -w "%{http_code}" -X POST "$B$1" "${H[@]}" -d "$2" "${@:3}"; }
t "tanpa cookie /akun -> redirect" "$(curl -s -o /dev/null -w '%{http_code}' $B/akun)" 307
t "Origin asing ditolak" "$(curl -s -o /dev/null -w '%{http_code}' -X POST $B/api/auth/login -H 'Origin: http://evil.test' -H 'Content-Type: application/json' -d '{}')" 403
REG=$(printf '{"type":"customer","name":"Smoke","email":"%s","password":"%s"}' "$E" "$P")
t "register 201" "$(post /api/auth/register "$REG" -c "$CJ")" 201
grep -q "HttpOnly.*st_session" $CJ && echo "PASS cookie httpOnly" || { echo "FAIL cookie httpOnly"; FAIL=1; }
t "/akun dengan cookie" "$(curl -s -b "$CJ" -o /dev/null -w '%{http_code}' $B/akun)" 200
t "cookie palsu ditolak" "$(curl -s -o /dev/null -w '%{http_code}' -b 'st_session=palsu;__Host-st_session=palsu' $B/akun)" 307
t "email dobel 409" "$(post /api/auth/register "$REG")" 409
A=$(curl -s -X POST $B/api/auth/login "${H[@]}" -d '{"email":"tak.ada@example.com","password":"x12345678"}')
BAD=$(printf '{"email":"%s","password":"salah-salah"}' "$E")
Bb=$(curl -s -X POST $B/api/auth/login "${H[@]}" -d "$BAD")
t "pesan login seragam" "$A" "$Bb"
t "logout" "$(post /api/auth/logout '{}' -b "$CJ" -c "$CJ")" 200
last=0; for i in 1 2 3 4 5 6 7 8; do last=$(post /api/auth/login '{"email":"rl@example.com","password":"x12345678"}'); done
t "rate limit 429" "$last" 429
rm -f $CJ; exit $FAIL
