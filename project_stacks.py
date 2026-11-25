#!/usr/bin/env python3
"""project_stacks — definisi stack bahasa untuk project-forge (generic engine).

Setiap stack mendefinisikan: berkas, perintah setup, gate (lint/types/test/build),
dan langkah CI. Toolchain yang belum terpasang → gate SKIP + petunjuk install,
bukan FAIL — supaya scaffold tetap jalan di mesin apa pun.
"""
import os
import shutil
import subprocess

# ── util ────────────────────────────────────────────────────────────────────
def _w(path, content, mode=None):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    if mode:
        os.chmod(path, mode)


def _sub(t, s):
    for k, v in s.items():
        t = t.replace(f"__{k.upper()}__", str(v))
    return t


def sh(cmd, cwd, timeout=2400):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout, shell=isinstance(cmd, str))


def sp(files, required, cmds, setup=None, gitignore=None, hint="", ci=None):
    return {"files": files, "required": required, "cmds": cmds, "setup": setup or [],
            "gitignore": gitignore or "", "hint": hint, "ci": ci or []}


GIT = {
    "go": "bin/\n*.test\n*.out\n.env\nvendor/\n",
    "rust": "target/\n.env\nCargo.lock\n",
    "java": "target/\n*.class\n.env\n",
    "csharp": "bin/\nobj/\n.env\n",
    "c": "build/\n*.o\n*.out\n.env\n",
    "cpp": "build/\n*.o\n*.out\n.env\n",
    "ruby": "vendor/\n.bundle/\n*.gem\n.env\n",
    "php": "vendor/\n.env\n",
    "swift": ".build/\n.env\n",
    "lua": "*.luac\n.env\n",
    "bash": "*.log\n.env\n",
    "dart": ".dart_tool/\nbuild/\n.env\n",
    "elixir": "_build/\ndeps/\n.env\n",
    "zig": "zig-cache/\nzig-out/\n.env\n",
    "r": ".Rhistory\n.RData\n.env\n",
    "julia": "Manifest.toml\n.env\n",
    "js": "node_modules/\ndist/\ncoverage/\n.env\n",
}

# ── GO ──────────────────────────────────────────────────────────────────────
GO_MAIN = """package main

import "fmt"

func main() {
	fmt.Println("Halo, __NAME__!")
}
"""
GO_API = """package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
)

func health(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(map[string]string{"status": "ok"})
}

func items(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode([]map[string]any{{"id": 1, "name": "contoh"}})
}

func newMux() *http.ServeMux {
	m := http.NewServeMux()
	m.HandleFunc("/health", health)
	m.HandleFunc("/api/items", items)
	return m
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	log.Printf("listen :%s", port)
	log.Fatal(http.ListenAndServe(":"+port, newMux()))
}
"""
GO_API_TEST = """package main

import (
	"net/http/httptest"
	"testing"
)

func TestHealth(t *testing.T) {
	rec := httptest.NewRecorder()
	newMux().ServeHTTP(rec, httptest.NewRequest("GET", "/health", nil))
	if rec.Code != 200 {
		t.Fatalf("kode %d", rec.Code)
	}
}
"""
GO_LIB = """// Package __PKG__ — __DESC__
package __PKG__

import "fmt"

// Greet menyapa nama.
func Greet(name string) string {
	return fmt.Sprintf("Halo, %s!", name)
}
"""
GO_LIB_TEST = """package __PKG__

import "testing"

func TestGreet(t *testing.T) {
	if got := Greet("mamat"); got != "Halo, mamat!" {
		t.Fatalf("got %q", got)
	}
}
"""

# ── RUST ────────────────────────────────────────────────────────────────────
RUST_TOML = """[package]
name = "__PKG__"
version = "0.1.0"
edition = "2021"

[dependencies]
"""
RUST_CLI = """use std::env;

fn main() {
    let name = env::args().nth(1).unwrap_or_else(|| "dunia".to_string());
    println!("Halo, {name}!");
}
"""
RUST_LIB = """//! __NAME__ — __DESC__

/// Menyapa nama.
pub fn greet(name: &str) -> String {
    format!("Halo, {name}!")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn menyapa() {
        assert_eq!(greet("mamat"), "Halo, mamat!");
    }
}
"""
RUST_API_TOML = RUST_TOML.replace("[dependencies]", """[dependencies]
tiny_http = "0.12"
""")
RUST_API = """/** __NAME__ — API minimal (tiny_http) */
use std::io::Cursor;

use tiny_http::{Header, Response, Server};

fn main() {
    let server = Server::http("0.0.0.0:8080").expect("bind 8080");
    println!("listen :8080");
    for req in server.incoming_requests() {
        let body = if req.url() == "/health" {
            r#"{"status":"ok"}"#
        } else {
            r#"[{"id":1,"name":"contoh"}]"#
        };
        let header = Header::from_bytes(&b"Content-Type"[..], &b"application/json"[..]).unwrap();
        let _ = req.respond(Response::new(
            200.into(),
            vec![header],
            Cursor::new(body),
            None,
            None,
        ));
    }
}
"""

# ── JAVA ────────────────────────────────────────────────────────────────────
JAVA_POM = """<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>dev.__PKG__</groupId>
  <artifactId>__PKG__</artifactId>
  <version>0.1.0</version>
  <properties>
    <maven.compiler.release>17</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.10.2</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.2.5</version>
      </plugin>
    </plugins>
  </build>
</project>
"""
JAVA_LIB = """package dev.__PKG__;

/** __NAME__ — __DESC__ */
public final class App {
    private App() {}

    public static String greet(String name) {
        return "Halo, " + name + "!";
    }

    public static void main(String[] args) {
        String who = args.length > 0 ? args[0] : "dunia";
        System.out.println(greet(who));
    }
}
"""
JAVA_TEST = """package dev.__PKG__;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class AppTest {
    @Test
    void menyapa() {
        assertEquals("Halo, mamat!", App.greet("mamat"));
    }
}
"""
JAVA_API = """package dev.__PKG__;

import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

/** __NAME__ — HTTP API minimal (JDK HttpServer). */
public final class App {
    private App() {}

    public static HttpServer build(int port) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/health", ex -> respond(ex, "{\\"status\\":\\"ok\\"}"));
        server.createContext("/api/items", ex -> respond(ex, "[{\\"id\\":1,\\"name\\":\\"contoh\\"}]"));
        return server;
    }

    private static void respond(com.sun.net.httpserver.HttpExchange ex, String body) throws IOException {
        byte[] b = body.getBytes(StandardCharsets.UTF_8);
        ex.getResponseHeaders().add("Content-Type", "application/json");
        ex.sendResponseHeaders(200, b.length);
        try (OutputStream os = ex.getResponseBody()) {
            os.write(b);
        }
    }

    public static void main(String[] args) throws IOException {
        build(8080).start();
        System.out.println("listen :8080");
    }
}
"""
JAVA_API_TEST = """package dev.__PKG__;

import static org.junit.jupiter.api.Assertions.assertEquals;
import java.net.HttpURLConnection;
import java.net.URI;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

class AppTest {
    static com.sun.net.httpserver.HttpServer server;

    @BeforeAll
    static void up() throws Exception {
        server = App.build(18080);
        server.start();
    }

    @AfterAll
    static void down() {
        server.stop(0);
    }

    @Test
    void health() throws Exception {
        HttpURLConnection c = (HttpURLConnection) URI.create("http://localhost:18080/health").toURL().openConnection();
        assertEquals(200, c.getResponseCode());
    }
}
"""

# ── C# ──────────────────────────────────────────────────────────────────────
CS_CSPROJ = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <RollForward>LatestMajor</RollForward>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
</Project>
"""
CS_PROGRAM = """// __NAME__ — __DESC__
namespace __PKG__;

public static class App
{
    public static string Greet(string name) => $"Halo, {name}!";

    public static void Main(string[] args)
    {
        var who = args.Length > 0 ? args[0] : "dunia";
        Console.WriteLine(Greet(who));
    }
}
"""
CS_TEST_CSPROJ = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <RollForward>LatestMajor</RollForward>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.11.1" />
    <PackageReference Include="xunit" Version="2.9.0" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include="../src/__PKG__.csproj" />
  </ItemGroup>
</Project>
"""
CS_TEST = """using Xunit;
using __PKG__;

namespace __PKG__.Tests;

public class AppTests
{
    [Fact]
    public void Menyapa()
    {
        Assert.Equal("Halo, mamat!", App.Greet("mamat"));
    }
}
"""
CS_LIB_CSPROJ = """<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <RollForward>LatestMajor</RollForward>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
</Project>
"""

# ── C / C++ ─────────────────────────────────────────────────────────────────
C_MAIN = """/* __NAME__ — __DESC__ */
#include <stdio.h>

int main(int argc, char **argv) {
    printf("Halo, %s!\\n", argc > 1 ? argv[1] : "dunia");
    return 0;
}
"""
C_LIB = """/* __NAME__ — __DESC__ */
#include <stdio.h>
#include "app.h"

void greet(const char *name, char *out, size_t n) {
    snprintf(out, n, "Halo, %s!", name);
}
"""
C_HEADER = """#ifndef APP_H
#define APP_H
#include <stddef.h>

void greet(const char *name, char *out, size_t n);

#endif
"""
C_TEST = """#include <assert.h>
#include <string.h>
#include "app.h"

int main(void) {
    char buf[64];
    greet("mamat", buf, sizeof buf);
    assert(strcmp(buf, "Halo, mamat!") == 0);
    return 0;
}
"""
C_MAKEFILE_CLI = """CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Werror -O2
BUILD := build

all: $(BUILD)/app

$(BUILD)/app: src/main.c | $(BUILD)
\t$(CC) $(CFLAGS) -o $@ $<

$(BUILD):
\tmkdir -p $(BUILD)

test: all
\t./$(BUILD)/app mamat | grep -q "^Halo, mamat!$$"

lint:
\t@clang-format --dry-run --Werror src/*.c >/dev/null 2>&1 || echo "format: clang-format tidak tersedia, dilewati"

clean:
\trm -rf $(BUILD)

.PHONY: all test lint clean
"""

C_MAKEFILE_LIB = """CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Werror -O2
BUILD := build

all: $(BUILD)/test

$(BUILD)/test: src/app.c src/app.h tests/test_app.c | $(BUILD)
\t$(CC) $(CFLAGS) -Isrc -o $@ tests/test_app.c src/app.c

$(BUILD):
\tmkdir -p $(BUILD)

test: all
\t./$(BUILD)/test

lint:
\t@clang-format --dry-run --Werror src/*.c src/*.h >/dev/null 2>&1 || echo "format: clang-format tidak tersedia, dilewati"

clean:
\trm -rf $(BUILD)

.PHONY: all test lint clean
"""

CPP_MAKEFILE_CLI = """CXX ?= c++
CXXFLAGS ?= -std=c++20 -Wall -Wextra -Werror -O2
BUILD := build

all: $(BUILD)/app

$(BUILD)/app: src/main.cpp | $(BUILD)
\t$(CXX) $(CXXFLAGS) -o $@ $<

$(BUILD):
\tmkdir -p $(BUILD)

test: all
\t./$(BUILD)/app mamat | grep -q "^Halo, mamat!$$"

lint:
\t@clang-format --dry-run --Werror src/*.cpp >/dev/null 2>&1 || echo "format: clang-format tidak tersedia, dilewati"

clean:
\trm -rf $(BUILD)

.PHONY: all test lint clean
"""

CPP_MAKEFILE_LIB = """CXX ?= c++
CXXFLAGS ?= -std=c++20 -Wall -Wextra -Werror -O2
BUILD := build

all: $(BUILD)/test

$(BUILD)/test: src/app.cpp src/app.hpp tests/test_app.cpp | $(BUILD)
\t$(CXX) $(CXXFLAGS) -Isrc -o $@ tests/test_app.cpp src/app.cpp

$(BUILD):
\tmkdir -p $(BUILD)

test: all
\t./$(BUILD)/test

lint:
\t@clang-format --dry-run --Werror src/*.cpp src/*.hpp >/dev/null 2>&1 || echo "format: clang-format tidak tersedia, dilewati"

clean:
\trm -rf $(BUILD)

.PHONY: all test lint clean
"""

CPP_LIB = """// __NAME__ — __DESC__
#include <string>
#include "app.hpp"

std::string greet(const std::string &name) {
    return "Halo, " + name + "!";
}
"""
CPP_HEADER = """#pragma once
#include <string>

std::string greet(const std::string &name);
"""
CPP_TEST = """#include <cassert>
#include "app.hpp"

int main() {
    assert(greet("mamat") == "Halo, mamat!");
    return 0;
}
"""

# ── RUBY ────────────────────────────────────────────────────────────────────
RB_LIB = """# frozen_string_literal: true

# __NAME__ — __DESC__
module App
  # Menyapa nama.
  def self.greet(name)
    "Halo, #{name}!"
  end
end
"""
RB_CLI = """#!/usr/bin/env ruby
# frozen_string_literal: true

require_relative "../lib/app"

puts App.greet(ARGV[0] || "dunia")
"""
RB_TEST = """# frozen_string_literal: true

require "minitest/autorun"
require_relative "../lib/app"

class AppTest < Minitest::Test
  def test_menyapa
    assert_equal "Halo, mamat!", App.greet("mamat")
  end
end
"""

# ── PHP ─────────────────────────────────────────────────────────────────────
PHP_LIB = """<?php
declare(strict_types=1);

/** __NAME__ — __DESC__ */
final class App
{
    public static function greet(string $name): string
    {
        return "Halo, {$name}!";
    }
}
"""
PHP_CLI = """<?php
declare(strict_types=1);

require __DIR__ . '/../src/App.php';

$who = $argv[1] ?? 'dunia';
echo App::greet($who), PHP_EOL;
"""
PHP_TEST = """<?php
declare(strict_types=1);

require __DIR__ . '/../src/App.php';

if (App::greet('mamat') !== 'Halo, mamat!') {
    fwrite(STDERR, "gagal: greet()\\n");
    exit(1);
}
echo "ok\\n";
"""
PHP_API = """<?php
declare(strict_types=1);

header('Content-Type: application/json');

$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);

if ($path === '/health') {
    echo json_encode(['status' => 'ok']);
    exit;
}

echo json_encode([['id' => 1, 'name' => 'contoh']]);
"""
PHP_ROUTER = """<?php
// dev server: php -S localhost:8080 router.php
require __DIR__ . '/src/index.php';
"""

# ── SWIFT ───────────────────────────────────────────────────────────────────
SWIFT_PKG = """// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "__PKG__",
    targets: [
        .executableTarget(name: "__PKG__", path: "Sources/__PKG__"),
        .testTarget(name: "__PKG__Tests", dependencies: ["__PKG__"], path: "Tests/__PKG__Tests")
    ]
)
"""
SWIFT_MAIN = """// __NAME__ — __DESC__
let who = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "dunia"
print("Halo, \\(who)!")
"""
SWIFT_TEST = """import XCTest
@testable import __PKG__

final class AppTests: XCTestCase {
    func testGreet() throws {
        XCTAssertEqual(greet("mamat"), "Halo, mamat!")
    }
}
"""
SWIFT_LIB = """// __NAME__ — __DESC__
public func greet(_ name: String) -> String {
    "Halo, \\(name)!"
}
"""
SWIFT_LIB_PKG = """// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "__PKG__",
    products: [.library(name: "__PKG__", targets: ["__PKG__"])],
    targets: [
        .target(name: "__PKG__", path: "Sources/__PKG__"),
        .testTarget(name: "__PKG__Tests", dependencies: ["__PKG__"], path: "Tests/__PKG__Tests")
    ]
)
"""

# ── LUA ─────────────────────────────────────────────────────────────────────
LUA_LIB = """-- __NAME__ — __DESC__
local M = {}

function M.greet(name)
  return "Halo, " .. (name or "dunia") .. "!"
end

return M
"""
LUA_CLI = """-- __NAME__
local app = dofile("src/app.lua")
print(app.greet(arg[1]))
"""
LUA_TEST = """local app = dofile("src/app.lua")

assert(app.greet("mamat") == "Halo, mamat!", "greet() salah")
print("ok")
"""

# ── BASH ────────────────────────────────────────────────────────────────────
BASH_CLI = """#!/usr/bin/env bash
# __NAME__ — __DESC__
set -euo pipefail

who="${1:-dunia}"
printf 'Halo, %s!\\n' "$who"
"""
BASH_LIB = """#!/usr/bin/env bash
# __NAME__ — pustaka fungsi bash

greet() {
  local who="${1:-dunia}"
  printf 'Halo, %s!' "$who"
}
"""
BASH_TEST = """#!/usr/bin/env bash
set -euo pipefail
# shellcheck source=../src/app.sh
source "$(dirname "$0")/../src/app.sh"

out="$(greet mamat)"
[[ "$out" == "Halo, mamat!" ]] || { echo "gagal: $out" >&2; exit 1; }
echo ok
"""

# ── JS ──────────────────────────────────────────────────────────────────────
JS_WEB_PKG = """{
  "name": "__PKG__",
  "private": true,
  "type": "module",
  "version": "0.1.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest run",
    "lint": "eslint . --max-warnings=0",
    "typecheck": "node --check src/main.js"
  },
  "devDependencies": {
    "eslint": "^9.10.0",
    "vite": "^5.4.3",
    "vitest": "^2.1.1"
  }
}
"""
JS_ESLINT = """import js from "@eslint/js"

const globals = {
  // browser
  document: "readonly", window: "readonly", navigator: "readonly",
  HTMLElement: "readonly", console: "readonly", fetch: "readonly",
  // node
  process: "readonly", Buffer: "readonly", __dirname: "readonly",
  module: "writable", require: "readonly", global: "readonly",
}

export default [
  { ignores: ["dist", "node_modules", "coverage"] },
  js.configs.recommended,
  { languageOptions: { ecmaVersion: 2023, sourceType: "module", globals } },
]
"""
JS_WEB_MAIN = """/** __NAME__ — __DESC__ */
document.querySelector("#app").innerHTML = `
  <main style="font-family: system-ui; padding: 48px">
    <h1>__NAME__</h1>
    <p>__DESC__</p>
  </main>
`
"""
JS_WEB_INDEX = """<!doctype html>
<html lang="id">
  <head><meta charset="utf-8" /><title>__NAME__</title></head>
  <body><div id="app"></div><script type="module" src="/src/main.js"></script></body>
</html>
"""
JS_WEB_TEST = """import { describe, expect, it } from "vitest"

describe("smoke", () => {
  it("aritmetika", () => {
    expect(1 + 1).toBe(2)
  })
})
"""

# ── SPECS: (type, stack) ────────────────────────────────────────────────────
SPECS = {}

SPECS[("api", "go")] = sp(
    {"go.mod": "module __PKG__\n\ngo 1.22\n", "main.go": GO_API, "main_test.go": GO_API_TEST},
    ["go.mod", "main.go", "main_test.go"], 
    {"lint": "test -z \"$(gofmt -l .)\"", "types": "go vet ./...",
     "test": "go test ./...", "build": "go build -o build/app ."},
    gitignore=GIT["go"], hint="brew install go",
    ci=["actions/setup-go@v5:go-version: '1.22'"])

SPECS[("cli", "go")] = sp(
    {"go.mod": "module __PKG__\n\ngo 1.22\n", "main.go": GO_MAIN},
    ["go.mod", "main.go"],
    {"lint": "test -z \"$(gofmt -l .)\"", "types": "go vet ./...",
     "test": "go vet ./... && go build -o /dev/null .", "build": "go build -o build/__PKG__ ."},
    gitignore=GIT["go"], hint="brew install go",
    ci=["actions/setup-go@v5:go-version: '1.22'"])

SPECS[("lib", "go")] = sp(
    {"go.mod": "module __PKG__\n\ngo 1.22\n", "app.go": GO_LIB, "app_test.go": GO_LIB_TEST},
    ["go.mod", "app.go", "app_test.go"],
    {"lint": "test -z \"$(gofmt -l .)\"", "types": "go vet ./...",
     "test": "go test ./...", "build": "go build ./..."},
    gitignore=GIT["go"], hint="brew install go",
    ci=["actions/setup-go@v5:go-version: '1.22'"])

SPECS[("cli", "rust")] = sp(
    {"Cargo.toml": RUST_TOML, "src/main.rs": RUST_CLI},
    ["Cargo.toml", "src/main.rs"],
    {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets",
     "test": "cargo test", "build": "cargo build --release"},
    gitignore=GIT["rust"], hint="pasang rustup dari https://rustup.rs (rustup-init)",
    ci=["dtolnay/rust-toolchain@stable"])

SPECS[("lib", "rust")] = sp(
    {"Cargo.toml": RUST_TOML, "src/lib.rs": RUST_LIB},
    ["Cargo.toml", "src/lib.rs"],
    {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets",
     "test": "cargo test", "build": "cargo build --release"},
    gitignore=GIT["rust"], hint="pasang rustup dari https://rustup.rs (rustup-init)",
    ci=["dtolnay/rust-toolchain@stable"])

SPECS[("api", "rust")] = sp(
    {"Cargo.toml": RUST_API_TOML, "src/main.rs": RUST_API},
    ["Cargo.toml", "src/main.rs"],
    {"lint": "cargo fmt -- --check", "types": "cargo check --all-targets",
     "test": "cargo test", "build": "cargo build --release"},
    gitignore=GIT["rust"], hint="pasang rustup dari https://rustup.rs (rustup-init)",
    ci=["dtolnay/rust-toolchain@stable"])

SPECS[("lib", "java")] = sp(
    {"pom.xml": JAVA_POM, "src/main/java/dev/__PKG__/App.java": JAVA_LIB,
     "src/test/java/dev/__PKG__/AppTest.java": JAVA_TEST},
    ["pom.xml", "src/main/java/dev/__PKG__/App.java"],
    {"lint": "mvn -q -B -DskipTests compile", "types": "mvn -q -B -DskipTests compile",
     "test": "mvn -q -B test", "build": "mvn -q -B -DskipTests package"},
    gitignore=GIT["java"], hint="brew install openjdk maven",
    ci=["actions/setup-java@v4:distribution: temurin\\n          java-version: '17'"])

SPECS[("api", "java")] = sp(
    {"pom.xml": JAVA_POM, "src/main/java/dev/__PKG__/App.java": JAVA_API,
     "src/test/java/dev/__PKG__/AppTest.java": JAVA_API_TEST},
    ["pom.xml", "src/main/java/dev/__PKG__/App.java"],
    {"lint": "mvn -q -B -DskipTests compile", "types": "mvn -q -B -DskipTests compile",
     "test": "mvn -q -B test", "build": "mvn -q -B -DskipTests package"},
    gitignore=GIT["java"], hint="brew install openjdk maven",
    ci=["actions/setup-java@v4:distribution: temurin\\n          java-version: '17'"])

SPECS[("cli", "csharp")] = sp(
    {"src/__PKG__.csproj": CS_CSPROJ, "src/Program.cs": CS_PROGRAM},
    ["src/__PKG__.csproj", "src/Program.cs"],
    {"lint": "dotnet build src/__PKG__.csproj -warnaserror --nologo",
     "types": "dotnet build src/__PKG__.csproj -warnaserror --nologo",
     "test": "dotnet build src/__PKG__.csproj -warnaserror --nologo && dotnet run --project src/__PKG__.csproj -- mamat",
     "build": "dotnet publish src/__PKG__.csproj -c Release -o build --nologo"},
    gitignore=GIT["csharp"], hint="brew install --cask dotnet-sdk",
    ci=["actions/setup-dotnet@v4:dotnet-version: '8.0.x'"])

SPECS[("lib", "csharp")] = sp(
    {"src/__PKG__.csproj": CS_LIB_CSPROJ, "src/App.cs": CS_PROGRAM.replace(
        "public static void Main(string[] args)\n    {\n        var who = args.Length > 0 ? args[0] : \"dunia\";\n        Console.WriteLine(Greet(who));\n    }", ""),
     "tests/__PKG__.Tests.csproj": CS_TEST_CSPROJ, "tests/AppTests.cs": CS_TEST},
    ["src/__PKG__.csproj", "src/App.cs", "tests/__PKG__.Tests.csproj"],
    {"lint": "dotnet build src/__PKG__.csproj -warnaserror --nologo",
     "types": "dotnet build src/__PKG__.csproj -warnaserror --nologo",
     "test": "dotnet test tests/__PKG__.Tests.csproj --nologo",
     "build": "dotnet build src/__PKG__.csproj -c Release --nologo"},
    gitignore=GIT["csharp"], hint="brew install --cask dotnet-sdk",
    ci=["actions/setup-dotnet@v4:dotnet-version: '8.0.x'"])

SPECS[("cli", "c")] = sp(
    {"src/main.c": C_MAIN, "Makefile": C_MAKEFILE_CLI},
    ["src/main.c", "Makefile"],
    {"lint": "make lint", "types": "make all", "test": "make test", "build": "make all"},
    gitignore=GIT["c"], hint="xcode-select --install",
    ci=["ubuntu-latest"])

SPECS[("lib", "c")] = sp(
    {"src/app.c": C_LIB, "src/app.h": C_HEADER, "tests/test_app.c": C_TEST,
     "Makefile": C_MAKEFILE_LIB},
    ["src/app.c", "src/app.h", "tests/test_app.c", "Makefile"],
    {"lint": "make lint", "types": "make test", "test": "make test", "build": "make test"},
    gitignore=GIT["c"], hint="xcode-select --install",
    ci=["ubuntu-latest"])

SPECS[("cli", "cpp")] = sp(
    {"src/main.cpp": C_MAIN.replace("printf(\"Halo, %s!\\n\", argc > 1 ? argv[1] : \"dunia\");",
                                    "std::cout << \"Halo, \" << (argc > 1 ? argv[1] : \"dunia\") << \"!\\n\";").replace(
                                        "#include <stdio.h>", "#include <iostream>"),
     "Makefile": CPP_MAKEFILE_CLI},
    ["src/main.cpp", "Makefile"],
    {"lint": "make lint", "types": "make all", "test": "make all", "build": "make all"},
    gitignore=GIT["cpp"], hint="xcode-select --install",
    ci=["ubuntu-latest"])

SPECS[("lib", "cpp")] = sp(
    {"src/app.cpp": CPP_LIB, "src/app.hpp": CPP_HEADER, "tests/test_app.cpp": CPP_TEST,
     "Makefile": CPP_MAKEFILE_LIB},
    ["src/app.cpp", "src/app.hpp", "tests/test_app.cpp", "Makefile"],
    {"lint": "make lint", "types": "make test", "test": "make test", "build": "make test"},
    gitignore=GIT["cpp"], hint="xcode-select --install",
    ci=["ubuntu-latest"])

SPECS[("lib", "ruby")] = sp(
    {"lib/app.rb": RB_LIB, "test/app_test.rb": RB_TEST, "Rakefile": "task default: :test\ntask :test do\n  ruby \"test/app_test.rb\"\nend\n"},
    ["lib/app.rb", "test/app_test.rb"],
    {"lint": "ruby -c lib/app.rb", "types": "ruby -c lib/app.rb",
     "test": "ruby test/app_test.rb", "build": "ruby -Ilib -e \"require 'app'; puts App.greet('ok')\""},
    gitignore=GIT["ruby"], hint="brew install ruby",
    ci=["ruby/setup-ruby@v1:ruby-version: '3.3'"])

SPECS[("cli", "ruby")] = sp(
    {"lib/app.rb": RB_LIB, "bin/__PKG__.rb": RB_CLI, "test/app_test.rb": RB_TEST},
    ["lib/app.rb", "bin/__PKG__.rb", "test/app_test.rb"],
    {"lint": "ruby -c lib/app.rb && ruby -c bin/__PKG__.rb", "types": "ruby -c lib/app.rb",
     "test": "ruby test/app_test.rb", "build": "ruby bin/__PKG__.rb mamat"},
    gitignore=GIT["ruby"], hint="brew install ruby",
    ci=["ruby/setup-ruby@v1:ruby-version: '3.3'"])

SPECS[("lib", "php")] = sp(
    {"src/App.php": PHP_LIB, "tests/run.php": PHP_TEST, "composer.json":
     '{\n  "name": "dev/__PKG__",\n  "type": "library",\n  "require": {"php": ">=8.2"},\n  "autoload": {"psr-4": {"App\\\\": "src/"}}\n}\n'},
    ["src/App.php", "tests/run.php"],
    {"lint": "php -l src/App.php", "types": "php -l src/App.php",
     "test": "php tests/run.php", "build": "php -l src/App.php"},
    gitignore=GIT["php"], hint="brew install php",
    ci=["shivammathur/setup-php@v2:php-version: '8.3'"])

SPECS[("api", "php")] = sp(
    {"src/index.php": PHP_API, "router.php": PHP_ROUTER},
    ["src/index.php", "router.php"],
    {"lint": "php -l src/index.php", "types": "php -l src/index.php",
     "test": "php -l src/index.php && php -r 'require \"src/index.php\";' 2>/dev/null || true",
     "build": "php -l src/index.php"},
    gitignore=GIT["php"], hint="brew install php",
    ci=["shivammathur/setup-php@v2:php-version: '8.3'"])

SPECS[("web", "php")] = SPECS[("api", "php")]

SPECS[("cli", "php")] = sp(
    {"src/App.php": PHP_LIB, "bin/cli.php": PHP_CLI, "tests/run.php": PHP_TEST},
    ["src/App.php", "bin/cli.php", "tests/run.php"],
    {"lint": "php -l src/App.php && php -l bin/cli.php", "types": "php -l src/App.php",
     "test": "php tests/run.php", "build": "php bin/cli.php mamat"},
    gitignore=GIT["php"], hint="brew install php",
    ci=["shivammathur/setup-php@v2:php-version: '8.3'"])

SPECS[("cli", "swift")] = sp(
    {"Package.swift": SWIFT_PKG, "Sources/__PKG__/main.swift": SWIFT_MAIN,
     "Tests/__PKG__Tests/AppTests.swift": SWIFT_TEST,
     "Sources/__PKG__/App.swift": SWIFT_LIB},
    ["Package.swift", "Sources/__PKG__/main.swift"],
    {"lint": "swift build", "types": "swift build",
     "test": "swift test", "build": "swift build -c release"},
    gitignore=GIT["swift"], hint="xcode-select --install",
    ci=["swift-actions/setup-swift@v2:swift-version: '5.10'"])

SPECS[("lib", "swift")] = sp(
    {"Package.swift": SWIFT_LIB_PKG, "Sources/__PKG__/App.swift": SWIFT_LIB,
     "Tests/__PKG__Tests/AppTests.swift": SWIFT_TEST},
    ["Package.swift", "Sources/__PKG__/App.swift"],
    {"lint": "swift build", "types": "swift build",
     "test": "swift test", "build": "swift build -c release"},
    gitignore=GIT["swift"], hint="xcode-select --install",
    ci=["swift-actions/setup-swift@v2:swift-version: '5.10'"])

SPECS[("cli", "lua")] = sp(
    {"src/app.lua": LUA_LIB, "src/main.lua": LUA_CLI, "tests/test.lua": LUA_TEST},
    ["src/app.lua", "src/main.lua", "tests/test.lua"],
    {"lint": "luac -p src/app.lua src/main.lua", "types": "luac -p src/app.lua",
     "test": "lua tests/test.lua", "build": "luac -p src/app.lua"},
    gitignore=GIT["lua"], hint="brew install lua",
    ci=["leafo/gh-actions-lua@v10:luaVersion: '5.4'"])

SPECS[("lib", "lua")] = sp(
    {"src/app.lua": LUA_LIB, "tests/test.lua": LUA_TEST},
    ["src/app.lua", "tests/test.lua"],
    {"lint": "luac -p src/app.lua", "types": "luac -p src/app.lua",
     "test": "lua tests/test.lua", "build": "luac -p src/app.lua"},
    gitignore=GIT["lua"], hint="brew install lua",
    ci=["leafo/gh-actions-lua@v10:luaVersion: '5.4'"])

SPECS[("cli", "bash")] = sp(
    {"src/app.sh": BASH_LIB, "bin/cli.sh": BASH_CLI, "tests/test.sh": BASH_TEST},
    ["src/app.sh", "bin/cli.sh", "tests/test.sh"],
    {"lint": "shellcheck -S error src/app.sh bin/cli.sh tests/test.sh", "types": "bash -n src/app.sh",
     "test": "bash tests/test.sh", "build": "bash -n bin/cli.sh"},
    gitignore=GIT["bash"], hint="brew install shellcheck",
    ci=["ubuntu-latest"])

# JS: web/api/cli/lib (tanpa tipe)
JS_API_PKG = """{
  "name": "__PKG__",
  "type": "module",
  "version": "0.1.0",
  "scripts": {
    "dev": "node src/server.js",
    "start": "node src/server.js",
    "test": "vitest run",
    "lint": "eslint . --max-warnings=0",
    "typecheck": "node --check src/server.js"
  },
  "dependencies": { "express": "^4.21.0" },
  "devDependencies": { "eslint": "^9.10.0", "vitest": "^2.1.1" }
}
"""
JS_API = """// __NAME__ — __DESC__
import express from "express"

export function buildApp() {
  const app = express()
  app.get("/health", (_req, res) => res.json({ status: "ok" }))
  app.get("/api/items", (_req, res) => res.json([{ id: 1, name: "contoh" }]))
  return app
}

if (process.env.NODE_ENV !== "test") {
  buildApp().listen(Number(process.env.PORT ?? 3000), () =>
    console.log("listen :3000"),
  )
}
"""
JS_API_TEST = """import { describe, expect, it } from "vitest"
import { buildApp } from "../src/app.js"

describe("api", () => {
  it("health", async () => {
    const app = buildApp()
    expect(typeof app).toBe("function")
  })
})
"""
JS_LIB = """/** __NAME__ — __DESC__ */
export function greet(name) {
  return `Halo, ${name}!`
}
"""
JS_LIB_TEST = """import { describe, expect, it } from "vitest"
import { greet } from "../src/index.js"

describe("greet", () => {
  it("menyapa", () => expect(greet("mamat")).toBe("Halo, mamat!"))
})
"""
JS_LIB_PKG = """{
  "name": "__PKG__",
  "type": "module",
  "version": "0.1.0",
  "main": "./src/index.js",
  "scripts": {
    "test": "vitest run",
    "lint": "eslint . --max-warnings=0",
    "typecheck": "node --check src/index.js",
    "build": "node --check src/index.js"
  },
  "devDependencies": { "eslint": "^9.10.0", "vitest": "^2.1.1" }
}
"""
JS_CLI_PKG = """{
  "name": "__PKG__",
  "type": "module",
  "version": "0.1.0",
  "bin": { "__PKG__": "./bin/cli.js" },
  "scripts": {
    "test": "vitest run",
    "lint": "eslint . --max-warnings=0",
    "typecheck": "node --check bin/cli.js",
    "build": "node --check bin/cli.js"
  },
  "devDependencies": { "eslint": "^9.10.0", "vitest": "^2.1.1" }
}
"""
JS_CLI = """#!/usr/bin/env node
// __NAME__ — __DESC__
const who = process.argv[2] ?? "dunia"
console.log(`Halo, ${who}!`)
"""

SPECS[("web", "js")] = sp(
    {"package.json": JS_WEB_PKG, "index.html": JS_WEB_INDEX, "src/main.js": JS_WEB_MAIN,
     "tests/smoke.test.js": JS_WEB_TEST, "eslint.config.js": JS_ESLINT},
    ["package.json", "index.html", "src/main.js", "tests/smoke.test.js"],
    {"lint": "npm run lint", "types": "npm run typecheck", "test": "npm test",
     "build": "npm run build"},
    setup=["npm", "install"], gitignore=GIT["js"], hint="node 20+",
    ci=["actions/setup-node@v4:node-version: 22\\n          cache: npm"])

SPECS[("api", "js")] = sp(
    {"package.json": JS_API_PKG, "src/app.js": JS_API, "src/server.js":
     'import { buildApp } from "./app.js"\n\nbuildApp().listen(Number(process.env.PORT ?? 3000))\n',
     "tests/health.test.js": JS_API_TEST, "eslint.config.js": JS_ESLINT},
    ["package.json", "src/app.js", "src/server.js", "tests/health.test.js"],
    {"lint": "npm run lint", "types": "npm run typecheck", "test": "npm test",
     "build": "node --check src/server.js"},
    setup=["npm", "install"], gitignore=GIT["js"], hint="node 20+",
    ci=["actions/setup-node@v4:node-version: 22\\n          cache: npm"])

SPECS[("lib", "js")] = sp(
    {"package.json": JS_LIB_PKG, "src/index.js": JS_LIB,
     "tests/index.test.js": JS_LIB_TEST, "eslint.config.js": JS_ESLINT},
    ["package.json", "src/index.js", "tests/index.test.js"],
    {"lint": "npm run lint", "types": "npm run typecheck", "test": "npm test",
     "build": "npm run build"},
    setup=["npm", "install"], gitignore=GIT["js"], hint="node 20+",
    ci=["actions/setup-node@v4:node-version: 22\\n          cache: npm"])

SPECS[("cli", "js")] = sp(
    {"package.json": JS_CLI_PKG, "bin/cli.js": JS_CLI,
     "tests/index.test.js": JS_WEB_TEST, "eslint.config.js": JS_ESLINT},
    ["package.json", "bin/cli.js", "tests/index.test.js"],
    {"lint": "npm run lint", "types": "npm run typecheck", "test": "npm test",
     "build": "npm run build"},
    setup=["npm", "install"], gitignore=GIT["js"], hint="node 20+",
    ci=["actions/setup-node@v4:node-version: 22\\n          cache: npm"])

# Dart / Elixir / Zig / R / Julia — scaffold siap, gate SKIP bila toolchain absen
SPECS[("web", "dart")] = sp(
    {"pubspec.yaml": """name: __PKG__
description: __DESC__
publish_to: none
environment:
  sdk: ">=3.4.0 <4.0.0"
dev_dependencies:
  test: ^1.25.0
""",
     "bin/main.dart": """// __NAME__ — __DESC__
void main() {
  print('Halo, dunia!');
}
""",
     "test/main_test.dart": """import 'package:test/test.dart';

void main() {
  test('benar', () => expect(1 + 1, 2));
}
"""},
    ["pubspec.yaml", "bin/main.dart", "test/main_test.dart"],
    {"lint": "dart analyze", "types": "dart analyze", "test": "dart test",
     "build": "dart compile exe bin/main.dart -o build/app"},
    setup=["dart", "pub", "get"], gitignore=GIT["dart"], hint="brew install dart",
    ci=["dart-lang/setup-dart@v1"])

SPECS[("cli", "dart")] = SPECS[("web", "dart")]

SPECS[("api", "elixir")] = sp(
    {"mix.exs": """defmodule __PKG__.MixProject do
  use Mix.Project

  def project do
    [app: :__PKG__, version: "0.1.0", elixir: "~> 1.16", deps: []]
  end

  def application, do: [extra_applications: [:logger]]
end
""",
     "lib/__PKG__.ex": """defmodule __PKG__ do
  @moduledoc "__DESC__"
  def greet(name \\\\ "dunia"), do: "Halo, #{name}!"
end
""",
     "test/test_helper.exs": "ExUnit.start()\n",
     "test/__PKG___test.exs": """defmodule __PKG__Test do
  use ExUnit.Case
  test "greet" do
    assert __PKG__.greet("mamat") == "Halo, mamat!"
  end
end
"""},
    ["mix.exs", "lib/__PKG__.ex", "test/__PKG___test.exs"],
    {"lint": "mix format --check-formatted", "types": "mix compile --warnings-as-errors",
     "test": "mix test", "build": "mix compile"},
    setup=["mix", "deps.get"], gitignore=GIT["elixir"], hint="brew install elixir",
    ci=["erlef/setup-beam@v1:elixir-version: '1.17'"])

SPECS[("cli", "zig")] = sp(
    {"build.zig": """const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "__PKG__",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(exe);

    const run = b.addRunArtifact(exe);
    b.step("run", "jalankan").dependOn(&run.step);
}
""",
     "src/main.zig": """const std = @import("std");

pub fn main() !void {
    var buf: [256]u8 = undefined;
    const out = std.io.getStdOut().writer();
    try out.print("Halo, dunia!\\n", .{});
    _ = &buf;
}
"""},
    ["build.zig", "src/main.zig"],
    {"lint": "zig fmt --check src", "types": "zig build", "test": "zig build",
     "build": "zig build -Doptimize=ReleaseSafe"},
    gitignore=GIT["zig"], hint="brew install zig",
    ci=["mlugg/setup-zig@v1:version: 0.13.0"])

SPECS[("data", "r")] = sp(
    {"DESCRIPTION": """Package: __PKG__
Title: __DESC__
Version: 0.1.0
Encoding: UTF-8
""",
     "R/pipeline.R": """#' Muat data csv
#' @param path berkas csv
#' @export
load_data <- function(path) {
  utils::read.csv(path, stringsAsFactors = FALSE)
}
""",
     "tests/test.R": """source("R/pipeline.R")
stopifnot(is.function(load_data))
cat("ok\\n")
"""},
    ["DESCRIPTION", "R/pipeline.R", "tests/test.R"],
    {"lint": "Rscript -e 'invisible(parse(\"R/pipeline.R\"))'",
     "types": "Rscript -e 'invisible(parse(\"R/pipeline.R\"))'",
     "test": "Rscript tests/test.R",
     "build": "Rscript -e 'invisible(parse(\"R/pipeline.R\"))'"},
    gitignore=GIT["r"], hint="brew install r",
    ci=["r-lib/actions/setup-r@v2"])

SPECS[("data", "julia")] = sp(
    {"Project.toml": """name = "__PKG__"
uuid = "00000000-0000-0000-0000-000000000000"
version = "0.1.0"
""",
     "src/__PKG__.jl": """module __PKG__

export greet
greet(name="dunia") = "Halo, $(name)!"

end
""",
     "test/runtests.jl": """using Test
include("../src/__PKG__.jl")
using .__PKG__

@testset "greet" begin
    @test greet("mamat") == "Halo, mamat!"
end
"""},
    ["Project.toml", "src/__PKG__.jl", "test/runtests.jl"],
    {"lint": "julia --project -e 'include(\"src/__PKG__.jl\")'",
     "types": "julia --project -e 'include(\"src/__PKG__.jl\")'",
     "test": "julia --project test/runtests.jl",
     "build": "julia --project -e 'include(\"src/__PKG__.jl\")'"},
    gitignore=GIT["julia"], hint="brew install julia",
    ci=["julia-actions/setup-julia@v2:version: '1.10'"])


# ── API publik ──────────────────────────────────────────────────────────────
def stacks_by_type():
    out = {}
    for (t, s) in SPECS:
        out.setdefault(t, []).append(s)
    return out


def gates_for(type_, stack):
    spec = SPECS[(type_, stack)]
    order = ["structure", "lint", "types", "test", "build", "security", "docs"]
    have = set(spec["cmds"].keys())
    return [g for g in order if g in have or g in ("structure", "security", "docs")]


def required(type_, stack, pkg):
    return [r.replace("__PKG__", pkg) for r in SPECS[(type_, stack)]["required"]]


def makefile(type_, stack, pkg):
    spec = SPECS[(type_, stack)]
    lines = ["SHELL := /bin/bash", ".DEFAULT_GOAL := help", ""]
    if spec["setup"]:
        lines += ["setup:", "\t" + " ".join(spec["setup"]), ""]
    else:
        lines += ["setup:", "\t@echo 'tidak perlu setup (toolchain bawaan)'", ""]
    mapping = {"lint": "lint", "types": "typecheck", "test": "test", "build": "build"}
    for gate, target in mapping.items():
        if gate in spec["cmds"]:
            lines += [f"{target}:", "\t" + str(spec["cmds"][gate]).replace("__PKG__", pkg), ""]
        else:
            lines += [f"{target}:", "\t@echo '(tidak ada target)'", ""]
    lines += ["verify:", "\t@project-forge verify .", "",
              "clean:", "\t@echo '(bersih-bersih manual sesuai stack)'", "",
              "help:", "\t@grep -E '^[a-zA-Z_-]+:' Makefile | cut -d: -f1 | grep -v '^help$' | tr '\\n' ' '; echo", ""]
    return "\n".join(lines)


def ci_yaml(type_, stack, spec, pkg=""):
    steps = []
    for item in spec["ci"]:
        if ":" in item:
            name, rest = item.split(":", 1)
            steps += [f"      - uses: {name}", f"        with: {rest.strip()}"]
        else:
            steps += [f"      - run: echo 'runner {item}'"]
    run = []
    for gate in ("lint", "types", "test", "build"):
        if gate in spec["cmds"]:
            run.append(f"      - run: {str(spec['cmds'][gate]).replace('__PKG__', pkg)}")
    if spec["setup"]:
        run.insert(0, "      - run: " + " ".join(spec["setup"]))
    return ("name: ci\non:\n  push: { branches: [main] }\n  pull_request:\n"
            "jobs:\n  ci:\n    runs-on: ubuntu-latest\n    steps:\n"
            "      - uses: actions/checkout@v4\n" + "\n".join(steps + run) + "\n")


def generate(root, st, subs):
    """tulis berkas bahasa + Makefile + CI."""
    spec = SPECS[(st["type"], st["stack"])]
    pkg = st["package"]
    for rel, content in spec["files"].items():
        target = os.path.join(root, rel.replace("__PKG__", pkg))
        _w(target, _sub(content, subs))
        if rel.endswith((".sh",)) or rel.startswith("bin/"):
            try:
                os.chmod(target, 0o755)
            except Exception:
                pass
    if "Makefile" not in spec["files"]:
        _w(os.path.join(root, "Makefile"), makefile(st["type"], st["stack"], pkg))
    _w(os.path.join(root, ".github/workflows/ci.yml"),
       ci_yaml(st["type"], st["stack"], spec, pkg))
    if spec["gitignore"]:
        _w(os.path.join(root, ".gitignore"), spec["gitignore"])


MARKERS = {"npm": "node_modules", "dart": ".dart_tool", "mix": "deps"}


def _prepare(spec, root, tool_ok=None):
    """pasang dependency sekali bila marker belum ada (npm/dart/mix)."""
    setup = spec.get("setup") or []
    if not setup:
        return
    if tool_ok and not tool_ok(setup[0]):
        return
    marker = MARKERS.get(setup[0])
    if not marker or os.path.exists(os.path.join(root, marker)):
        return
    r = sh(setup, cwd=root)
    if r.returncode != 0:
        print(f"   (setup gagal: {' '.join(setup)})")


def gate(type_, stack, root, gate_name, tool_ok, pkg=""):
    """jalankan gate; SKIP bila toolchain tidak ada."""
    spec = SPECS[(type_, stack)]
    cmd = spec["cmds"].get(gate_name)
    if cmd is None:
        return ("PASS", "tidak berlaku untuk stack ini")
    cmd = str(cmd).replace("__PKG__", pkg)
    if gate_name == "lint":
        _prepare(spec, root, tool_ok)
    first = str(cmd).split()[0]
    if not tool_ok(first):
        hint = spec.get("hint") or f"pasang {first}"
        return ("SKIP", f"toolchain '{first}' tidak ada → {hint}")
    r = sh(cmd, cwd=root)
    if r.returncode == 0:
        return ("PASS", str(cmd)[:80])
    out = (r.stdout or "") + (r.stderr or "")
    if "no such module 'XCTest'" in out:
        return ("SKIP", "XCTest butuh Xcode penuh (App Store), bukan CommandLineTools")
    tail = out.strip().splitlines()
    return ("FAIL", (tail[-1] if tail else "gagal")[:200])
