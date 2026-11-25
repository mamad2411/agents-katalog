#!/usr/bin/env bash
# Uji asap area penonton. Pakai: customer-smoke.sh http://localhost:3100 email sandi
B=${1:-http://localhost:3100}; E=${2:-pengguna@gmail.com}; P=${3:-Pengguna123!}; CJ=$(mktemp); F=0
t(){ [ "$2" = "$3" ] && echo "PASS $1" || { echo "FAIL $1 (dapat '$2', harap '$3')"; F=1; }; }
code(){ curl -s -o /dev/null -w "%{http_code}" "$@"; }
for p in /beranda /konser /tiket-saya /riwayat /tiket-disimpan /pengaturan; do t "tanpa cookie $p -> 307" "$(code $B$p)" 307; done
curl -s -c "$CJ" -o /dev/null -X POST $B/api/auth/login -H "Origin: $B" -H 'Content-Type: application/json' -d "{\"email\":\"$E\",\"password\":\"$P\"}"
for p in /beranda /konser "/konser?q=raisa" "/konser?price=gt500" /tiket-saya /riwayat /tiket-disimpan /pengaturan; do t "login $p -> 200" "$(code -b "$CJ" "$B$p")" 200; done
t "BFF notifikasi 200" "$(code -b "$CJ" $B/api/customer/notifications)" 200
t "BFF rute di luar allowlist 404" "$(code -b "$CJ" $B/api/customer/admin/x)" 404
t "BFF POST tanpa Origin 403" "$(code -b "$CJ" -X POST $B/api/customer/favorites/1)" 403
t "PDF tiket 200" "$(code -b "$CJ" $B/api/customer/tickets/1/pdf)" 200
rm -f "$CJ"; exit $F
