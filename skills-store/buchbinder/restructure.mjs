import fs from 'fs-extra';
import path from 'path';

const base = 'src/templates';

// 1. Rename constitute -> manifest
if (fs.existsSync('src/templates/base/constitution.md')) {
  fs.moveSync('src/templates/base/constitution.md', 'src/templates/base/manifest.md', { overwrite: true });
}
if (fs.existsSync('src/tools/hubs/buchbinder/constitute.ts')) {
  fs.moveSync('src/tools/hubs/buchbinder/constitute.ts', 'src/tools/hubs/buchbinder/manifest.ts', { overwrite: true });
}

// 2. Metadata directories
fs.ensureDirSync('src/templates/fiction/metadata');
fs.ensureDirSync('src/templates/non-fiction/metadata');
fs.ensureDirSync('src/templates/non-fiction/research');
fs.ensureDirSync('src/templates/series/lorebook');

// 3. Move/Create metadata files
if (fs.existsSync('src/templates/base/style-sheet/formatting.md')) {
  fs.copySync('src/templates/base/style-sheet/formatting.md', 'src/templates/fiction/metadata/formatting.md');
  fs.moveSync('src/templates/base/style-sheet/formatting.md', 'src/templates/non-fiction/metadata/formatting.md', { overwrite: true });
}

fs.writeFileSync('src/templates/fiction/metadata/tone.md', '# Tone\n\n*Fiction narrative tone directives.*\n');
fs.writeFileSync('src/templates/non-fiction/metadata/tone.md', '# Tone\n\n*Non-fiction narrative tone directives.*\n');

if (fs.existsSync('src/templates/base/style-sheet/emotional-register.md')) fs.moveSync('src/templates/base/style-sheet/emotional-register.md', 'src/templates/fiction/metadata/emotional-register.md', { overwrite: true });
if (fs.existsSync('src/templates/base/style-sheet/character-voices.md')) fs.moveSync('src/templates/base/style-sheet/character-voices.md', 'src/templates/fiction/metadata/character-voices.md', { overwrite: true });
if (fs.existsSync('src/templates/base/style-sheet/terminology.md')) fs.moveSync('src/templates/base/style-sheet/terminology.md', 'src/templates/non-fiction/research/terminology.md', { overwrite: true });

fs.writeFileSync('src/templates/fiction/metadata/plot-tracker.md', '# Plot Tracker\n\n*Compressed outline and plot state.*\n');
fs.writeFileSync('src/templates/fiction/metadata/relationships.md', '# Relationships\n\n*Character relationship dynamics.*\n');
fs.writeFileSync('src/templates/fiction/metadata/timeline.md', '# Timeline\n\n*Broad course of events/epoch context.*\n');
fs.writeFileSync('src/templates/fiction/metadata/validation-rules.md', '# Validation Rules\n\n*Rules for QA and continuity.*\n');

// Cleanup old templates
fs.removeSync('src/templates/base/style-sheet');
fs.removeSync('src/templates/fiction/tracking');

// Rename style-sheet.ts
if (fs.existsSync('src/lib/style-sheet.ts')) {
  fs.moveSync('src/lib/style-sheet.ts', 'src/lib/project-metadata.ts', { overwrite: true });
}
