---
alwaysApply: false
---
# Documentation Philosophy

●philosophy|ref:documentation_philosophy.mdc|frame:Ω:CONSTRUCTION|persona:P:ARCH
→purpose|ssot:documentation_lifecycle|reference:this_file|never:repeat_content

## Core Principle: Living Documentation, Not Dead Files

●principle|core:living_artifact|mandate:process_consolidate_evolve|never:create_unreferenced|never:keep_dead
→rule|documentation:living_not_static|action:process_after_completion|action:consolidate_to_rules|action:delete_when_extracted

## Documentation Lifecycle

●lifecycle|frame:Ω:CONSTRUCTION|stages:5
→stage1:create|when:necessary_only|method:consolidate_when_possible
→stage2:use|action:reference_during_execution|method:active_reference
→stage3:process|action:extract_learnings|timing:after_completion
→stage4:consolidate|target:rules_patterns|method:merge_learnings
→stage5:delete|when:learnings_extracted|when:no_longer_referenced

## Parallel Command Output Rule

●rule|id:parallel_output|critical:true|frame:Ω:SURGERY
→mandate|parallel_commands:single_doc|never:multiple_separate
→pattern|doc:single_consolidated|sections:per_command|context:shared|duplication:none|reference:single_point

○example|commands:run_planner_run_mobile_friendliness|output:one_doc_not_two

## Username Convention

●convention|id:username_placeholder|mandatory:true
→rule|never:hardcode_usernames|always:use_placeholder
→placeholder|format:[user name]|format:user name|never:actual_username

○examples|correct:plans/[user name]/active|correct:plans/user name/active|wrong:plans/ariahan/active

## Documentation Categories

●categories|frame:Ω:CONSTRUCTION|types:3

### **Active (Temporary)**

●category|type:active|temporary:true
→location|path:plans/[user name]/active/[category]/
→purpose|work_in_progress:true|execution_tracking:true
→lifecycle|create→use→process→delete
→examples|blueprints:true|reviews:true|mobile_audits:true|translation_audits:true

### **Rules (Permanent)**

●category|type:rules|permanent:true
→location|path:rules/
→purpose|patterns:long_term|laws:long_term|principles:long_term
→lifecycle|create→update→reference_forever
→examples|patterns.mdc:true|translation_patterns.md:true|mobile_friendliness_patterns.mdc:true

### **Commands (Permanent)**

●category|type:commands|permanent:true
→location|path:commands/
→purpose|persona_workflows:true|execution_protocols:true
→lifecycle|create→update→reference_forever
→examples|run_planner.md:true|run_review.md:true

## Consolidation Criteria

●criteria|frame:Ω:GARDENING|action:consolidate_or_delete

### Delete Active Docs When

●delete_when|conditions:5
→condition1|learnings:extracted_to_rules|status:complete
→condition2|referenced:no_longer_active|status:orphaned
→condition3|superseded:comprehensive_version|status:replaced
→condition4|duplicate:existing_doc|status:redundant
→condition5|completed:gt_30_days|exception:unique_learnings

### Preserve Active Docs When:

●preserve_when|conditions:4
→condition1|status:ACTIVE|execution:current
→condition2|completed:lt_30_days|recent:true
→condition3|learnings:unique_not_documented|value:preserved
→condition4|referenced:other_active_work|dependency:exists

### Consolidate Into Rules When:

●consolidate_when|conditions:4
→condition1|pattern:appears_3_plus_times|frequency:high
→condition2|learning:applies_broadly|scope:general
→condition3|anti_pattern:identified|prevention:needed
→condition4|process:improvement_discovered|value:system_wide

## Documentation Creation Rules

●creation_rules|frame:Ω:CONSTRUCTION|phases:3

### Before Creating ANY Doc:

●before_create|checklist:7|law:L:I
→step1|action:check_existing|method:grep_topic|path:plans/[user name]/active/
→step2|action:update_existing|never:create_new_if_exists
→step3|action:coordinate_parallel|output:single_doc|never:multiple_separate
→step4|action:use_folder_structure|path:plans/[user name]/active/[category]/
→step5|action:include_status|tracking:ACTIVE→COMPLETE→DELETED
→step6|action:include_consolidation_plan|target:where_learnings_go
→step7|action:use_placeholder|format:[user name]|never:hardcode

### During Creation:

●during_creation|rules:4
→rule1|reference:existing_rules_patterns|never:repeat_content
→rule2|placeholders:user_name|never:hardcode
→rule3|consolidation_plan:required|target:where_learnings_go
→rule4|status:mark_with|completion_criteria:include

### After Completion:

●after_completion|actions:4
→action1|extract:learnings_to_rules_patterns|target:long_term_knowledge
→action2|update:related_commands|if:process_improved
→action3|delete:doc_when_extracted|when:learnings_consolidated
→action4|document:deletion_in_audit|if:significant

## Anti-Patterns (Wall of Shame)

●anti_patterns|frame:Ω:SURGERY|purpose:prevent_repetition
→pattern1|❌multiple_docs:same_task|violation:duplication
→pattern2|❌hardcoding:usernames|violation:convention
→pattern3|❌no_consolidation_plan|violation:planning
→pattern4|❌keeping_completed:indefinitely|violation:lifecycle
→pattern5|❌repeating:rules_content|violation:ssot
→pattern6|❌creating_unreferenced|violation:purpose

## Verification Checklist

●verification|frame:Ω:SURGERY|phases:2

### Before Creating Doc:

●checklist_before|items:5
→item1|checked:existing_docs_on_topic|status:verified
→item2|coordinated:parallel_commands|output:single_doc
→item3|used:placeholder_[user name]|never:hardcode
→item4|referenced:existing_rules|duplication:none
→item5|included:consolidation_plan|target:defined

### After Completing Work:

●checklist_after|items:4
→item1|extracted:learnings_to_rules_patterns|status:consolidated
→item2|updated:commands_if_improved|process:enhanced
→item3|deleted:doc_or_marked|lifecycle:complete
→item4|documented:deletion_in_audit|if:significant
