#!/usr/bin/env python3
"""
Run after `npx cap add android`. Injects a release signingConfig into
android/app/build.gradle that reads the keystore from environment
variables (set from GitHub Actions secrets) rather than from any file
committed to the repo, and bumps versionCode/versionName if given.

Usage: python3 scripts/patch_gradle.py [versionCode] [versionName]
"""
import re
import sys
import os

GRADLE_PATH = os.path.join("android", "app", "build.gradle")

with open(GRADLE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

if "RELEASE_STORE_FILE" in content:
    print("build.gradle already patched, skipping signing-config injection.")
else:
    signing_block = """
    signingConfigs {
        release {
            storeFile file(System.getenv("RELEASE_STORE_FILE") ?: "release.keystore")
            storePassword System.getenv("RELEASE_STORE_PASSWORD")
            keyAlias System.getenv("RELEASE_KEY_ALIAS")
            keyPassword System.getenv("RELEASE_KEY_PASSWORD")
        }
    }
"""
    # Insert signingConfigs block right after the first "android {" line.
    content = re.sub(r"(android\s*\{)", r"\1" + signing_block, content, count=1)

    # Point the release build type at that signing config.
    content = re.sub(
        r"(buildTypes\s*\{\s*release\s*\{)",
        r"\1\n            signingConfig signingConfigs.release",
        content,
        count=1,
    )

if len(sys.argv) >= 2 and sys.argv[1]:
    content = re.sub(r"versionCode\s+\d+", f"versionCode {sys.argv[1]}", content)
if len(sys.argv) >= 3 and sys.argv[2]:
    content = re.sub(r'versionName\s+"[^"]*"', f'versionName "{sys.argv[2]}"', content)

with open(GRADLE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("build.gradle patched successfully.")
print(content)
