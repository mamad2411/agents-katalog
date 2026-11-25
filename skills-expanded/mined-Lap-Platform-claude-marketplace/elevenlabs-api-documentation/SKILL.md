---
name: elevenlabs-api-documentation
description: "ElevenLabs API Documentation API skill. Use when working with ElevenLabs API Documentation for history, sound-generation, audio-isolation. Covers 258 endpoints."
version: 1.0.0
generator: lapsh
---

# ElevenLabs API Documentation
API version: 1.0

## Auth
ApiKey xi-api-key in header

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /v1/history -- verify access
3. POST /v1/history/download -- create first download

## Endpoints

258 endpoints across 25 groups. See references/api-spec.lap for full details.

### history
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/history | List Generated Items |
| GET | /v1/history/{history_item_id} | Get History Item |
| DELETE | /v1/history/{history_item_id} | Delete History Item |
| GET | /v1/history/{history_item_id}/audio | Get Audio From History Item |
| POST | /v1/history/download | Download History Items |

### sound-generation
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/sound-generation | Sound Generation |

### audio-isolation
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/audio-isolation | Audio Isolation |
| POST | /v1/audio-isolation/stream | Audio Isolation Stream |

### voices
| Method | Path | Description |
|--------|------|-------------|
| DELETE | /v1/voices/{voice_id}/samples/{sample_id} | Delete Sample |
| GET | /v1/voices/{voice_id}/samples/{sample_id}/audio | Get Audio From Sample |
| GET | /v1/voices | List Voices |
| GET | /v2/voices | Get Voices V2 |
| GET | /v1/voices/settings/default | Get Default Voice Settings. |
| GET | /v1/voices/{voice_id}/settings | Get Voice Settings |
| GET | /v1/voices/{voice_id} | Get Voice |
| DELETE | /v1/voices/{voice_id} | Delete Voice |
| POST | /v1/voices/{voice_id}/settings/edit | Edit Voice Settings |
| POST | /v1/voices/add | Add Voice |
| POST | /v1/voices/{voice_id}/edit | Edit Voice |
| POST | /v1/voices/add/{public_user_id}/{voice_id} | Add Shared Voice |
| POST | /v1/voices/pvc | Create Pvc Voice |
| POST | /v1/voices/pvc/{voice_id} | Edit Pvc Voice |
| POST | /v1/voices/pvc/{voice_id}/samples | Add Samples To Pvc Voice |
| POST | /v1/voices/pvc/{voice_id}/samples/{sample_id} | Update Pvc Voice Sample |
| DELETE | /v1/voices/pvc/{voice_id}/samples/{sample_id} | Delete Pvc Voice Sample |
| GET | /v1/voices/pvc/{voice_id}/samples/{sample_id}/audio | Retrieve Voice Sample Audio |
| GET | /v1/voices/pvc/{voice_id}/samples/{sample_id}/waveform | Retrieve Voice Sample Visual Waveform |
| GET | /v1/voices/pvc/{voice_id}/samples/{sample_id}/speakers | Retrieve Speaker Separation Status |
| POST | /v1/voices/pvc/{voice_id}/samples/{sample_id}/separate-speakers | Start Speaker Separation |
| GET | /v1/voices/pvc/{voice_id}/samples/{sample_id}/speakers/{speaker_id}/audio | Retrieve Separated Speaker Audio |
| GET | /v1/voices/pvc/{voice_id}/captcha | Get Pvc Voice Captcha |
| POST | /v1/voices/pvc/{voice_id}/captcha | Verify Pvc Voice Captcha |
| POST | /v1/voices/pvc/{voice_id}/train | Run Pvc Training |
| POST | /v1/voices/pvc/{voice_id}/verification | Request Manual Verification |

### text-to-speech
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/text-to-speech/{voice_id} | Text To Speech |
| POST | /v1/text-to-speech/{voice_id}/with-timestamps | Text To Speech With Timestamps |
| POST | /v1/text-to-speech/{voice_id}/stream | Text To Speech Streaming |
| POST | /v1/text-to-speech/{voice_id}/stream/with-timestamps | Text To Speech Streaming With Timestamps |

### text-to-dialogue
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/text-to-dialogue | Text To Dialogue (Multi-Voice) |
| POST | /v1/text-to-dialogue/stream | Text To Dialogue (Multi-Voice) Streaming |
| POST | /v1/text-to-dialogue/stream/with-timestamps | Text To Dialogue Streaming With Timestamps |
| POST | /v1/text-to-dialogue/with-timestamps | Text To Dialogue With Timestamps |

### speech-to-speech
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/speech-to-speech/{voice_id} | Speech To Speech |
| POST | /v1/speech-to-speech/{voice_id}/stream | Speech To Speech Streaming |

### text-to-voice
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/text-to-voice/create-previews | Generate A Voice Preview From Description |
| POST | /v1/text-to-voice | Create A New Voice From Voice Preview |
| POST | /v1/text-to-voice/design | Design A Voice. |
| POST | /v1/text-to-voice/{voice_id}/remix | Remix A Voice. |
| GET | /v1/text-to-voice/{generated_voice_id}/stream | Text To Voice Preview Streaming |

### user
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/user/subscription | Get User Subscription Info |
| GET | /v1/user | Get User Info |

### studio
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/studio/podcasts | Create Podcast |
| POST | /v1/studio/projects/{project_id}/pronunciation-dictionaries | Create Pronunciation Dictionaries |
| GET | /v1/studio/projects | List Studio Projects |
| POST | /v1/studio/projects | Create Studio Project |
| POST | /v1/studio/projects/{project_id} | Update Studio Project |
| GET | /v1/studio/projects/{project_id} | Get Studio Project |
| DELETE | /v1/studio/projects/{project_id} | Delete Studio Project |
| POST | /v1/studio/projects/{project_id}/content | Update Studio Project Content |
| POST | /v1/studio/projects/{project_id}/convert | Convert Studio Project |
| GET | /v1/studio/projects/{project_id}/snapshots | List Studio Project Snapshots |
| GET | /v1/studio/projects/{project_id}/snapshots/{project_snapshot_id} | Get Project Snapshot |
| POST | /v1/studio/projects/{project_id}/snapshots/{project_snapshot_id}/stream | Stream Studio Project Audio |
| POST | /v1/studio/projects/{project_id}/snapshots/{project_snapshot_id}/archive | Stream Archive With Studio Project Audio |
| GET | /v1/studio/projects/{project_id}/chapters | List Chapters |
| POST | /v1/studio/projects/{project_id}/chapters | Create Chapter |
| GET | /v1/studio/projects/{project_id}/chapters/{chapter_id} | Get Chapter |
| POST | /v1/studio/projects/{project_id}/chapters/{chapter_id} | Update Chapter |
| DELETE | /v1/studio/projects/{project_id}/chapters/{chapter_id} | Delete Chapter |
| POST | /v1/studio/projects/{project_id}/chapters/{chapter_id}/convert | Convert Chapter |
| GET | /v1/studio/projects/{project_id}/chapters/{chapter_id}/snapshots | List Chapter Snapshots |
| GET | /v1/studio/projects/{project_id}/chapters/{chapter_id}/snapshots/{chapter_snapshot_id} | Get Chapter Snapshot |
| POST | /v1/studio/projects/{project_id}/chapters/{chapter_id}/snapshots/{chapter_snapshot_id}/stream | Stream Chapter Audio |
| GET | /v1/studio/projects/{project_id}/muted-tracks | Get Project Muted Tracks |

### dubbing
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/dubbing/resource/{dubbing_id} | Get The Dubbing Resource For An Id. |
| POST | /v1/dubbing/resource/{dubbing_id}/language | Add A Language To The Resource |
| POST | /v1/dubbing/resource/{dubbing_id}/speaker/{speaker_id}/segment | Create A Segment For The Speaker |
| PATCH | /v1/dubbing/resource/{dubbing_id}/segment/{segment_id}/{language} | Modify A Single Segment |
| POST | /v1/dubbing/resource/{dubbing_id}/migrate-segments | Move Segments Between Speakers |
| DELETE | /v1/dubbing/resource/{dubbing_id}/segment/{segment_id} | Deletes A Single Segment |
| POST | /v1/dubbing/resource/{dubbing_id}/transcribe | Transcribes Segments |
| POST | /v1/dubbing/resource/{dubbing_id}/translate | Translates All Or Some Segments And Languages |
| POST | /v1/dubbing/resource/{dubbing_id}/dub | Dubs All Or Some Segments And Languages |
| PATCH | /v1/dubbing/resource/{dubbing_id}/speaker/{speaker_id} | Update Metadata For A Speaker |
| POST | /v1/dubbing/resource/{dubbing_id}/speaker | Create A New Speaker |
| GET | /v1/dubbing/resource/{dubbing_id}/speaker/{speaker_id}/similar-voices | Search The Elevenlabs Library For Voices Similar To A Speaker. |
| POST | /v1/dubbing/resource/{dubbing_id}/render/{language} | Render Audio Or Video For The Given Language |
| GET | /v1/dubbing | List Dubs |
| POST | /v1/dubbing | Dub A Video Or An Audio File |
| GET | /v1/dubbing/{dubbing_id} | Get Dubbing |
| DELETE | /v1/dubbing/{dubbing_id} | Delete Dubbing |
| GET | /v1/dubbing/{dubbing_id}/audio/{language_code} | Get Dubbed File |
| GET | /v1/dubbing/{dubbing_id}/transcript/{language_code} | Get Dubbed Transcript |
| GET | /v1/dubbing/{dubbing_id}/transcripts/{language_code}/format/{format_type} | Retrieve A Transcript |

### models
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/models | Get Models |

### audio-native
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/audio-native | Creates Audio Native Enabled Project. |
| GET | /v1/audio-native/{project_id}/settings | Get Audio Native Project Settings |
| POST | /v1/audio-native/{project_id}/content | Update Audio-Native Project Content |
| POST | /v1/audio-native/content | Update Audio-Native Content From Url |

### shared-voices
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/shared-voices | Get Voices |

### similar-voices
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/similar-voices | Get Similar Library Voices |

### usage
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/usage/character-stats | Get Characters Usage Metrics |

### pronunciation-dictionaries
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/pronunciation-dictionaries/add-from-file | Add A Pronunciation Dictionary |
| POST | /v1/pronunciation-dictionaries/add-from-rules | Add A Pronunciation Dictionary |
| PATCH | /v1/pronunciation-dictionaries/{pronunciation_dictionary_id} | Update Pronunciation Dictionary |
| GET | /v1/pronunciation-dictionaries/{pronunciation_dictionary_id} | Get Metadata For A Pronunciation Dictionary |
| POST | /v1/pronunciation-dictionaries/{pronunciation_dictionary_id}/set-rules | Set Rules On The Pronunciation Dictionary |
| POST | /v1/pronunciation-dictionaries/{pronunciation_dictionary_id}/add-rules | Add Rules To The Pronunciation Dictionary |
| POST | /v1/pronunciation-dictionaries/{pronunciation_dictionary_id}/remove-rules | Remove Rules From The Pronunciation Dictionary |
| GET | /v1/pronunciation-dictionaries/{dictionary_id}/{version_id}/download | Get A Pls File With A Pronunciation Dictionary Version Rules |
| GET | /v1/pronunciation-dictionaries | Get Pronunciation Dictionaries |

### service-accounts
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/service-accounts/{service_account_user_id}/api-keys | Get Service Account Api Keys Route |
| POST | /v1/service-accounts/{service_account_user_id}/api-keys | Create Service Account Api Key |
| PATCH | /v1/service-accounts/{service_account_user_id}/api-keys/{api_key_id} | Edit Service Account Api Key |
| DELETE | /v1/service-accounts/{service_account_user_id}/api-keys/{api_key_id} | Delete Service Account Api Key |
| GET | /v1/service-accounts | Get Workspace Service Accounts |

### workspace
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/workspace/groups/search | Search User Groups |
| POST | /v1/workspace/groups/{group_id}/members/remove | Delete Member From User Group |
| POST | /v1/workspace/groups/{group_id}/members | Add Member To User Group |
| POST | /v1/workspace/invites/add | Invite User |
| POST | /v1/workspace/invites/add-bulk | Invite Multiple Users |
| DELETE | /v1/workspace/invites | Delete Existing Invitation |
| POST | /v1/workspace/members | Update Member |
| GET | /v1/workspace/resources/{resource_id} | Get Resource |
| POST | /v1/workspace/resources/{resource_id}/share | Share Workspace Resource |
| POST | /v1/workspace/resources/{resource_id}/unshare | Unshare Workspace Resource |
| GET | /v1/workspace/webhooks | List Workspace Webhooks |
| POST | /v1/workspace/webhooks | Create Workspace Webhook |
| PATCH | /v1/workspace/webhooks/{webhook_id} | Update Workspace Webhook |
| DELETE | /v1/workspace/webhooks/{webhook_id} | Delete Workspace Webhook |

### speech-to-text
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/speech-to-text | Speech To Text |
| GET | /v1/speech-to-text/transcripts/{transcription_id} | Get Transcript By Id |
| DELETE | /v1/speech-to-text/transcripts/{transcription_id} | Delete Transcript By Id |

### single-use-token
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/single-use-token/{token_type} | Create Single Use Token |

### forced-alignment
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/forced-alignment | Create Forced Alignment |

### convai
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/convai/conversation/get-signed-url | Get Signed Url |
| GET | /v1/convai/conversation/get_signed_url | Get Signed Url |
| GET | /v1/convai/conversation/token | Get Webrtc Token |
| POST | /v1/convai/twilio/outbound-call | Handle An Outbound Call Via Twilio |
| POST | /v1/convai/twilio/register-call | Register A Twilio Call And Return Twiml |
| POST | /v1/convai/whatsapp/outbound-call | Make An Outbound Call Via Whatsapp |
| POST | /v1/convai/whatsapp/outbound-message | Send An Outbound Message Via Whatsapp |
| POST | /v1/convai/agents/create | Create Agent |
| GET | /v1/convai/agents/summaries | Get Agent Summaries |
| GET | /v1/convai/agents/{agent_id} | Get Agent |
| PATCH | /v1/convai/agents/{agent_id} | Patches An Agent Settings |
| DELETE | /v1/convai/agents/{agent_id} | Delete Agent |
| GET | /v1/convai/agents/{agent_id}/widget | Get Agent Widget Config |
| GET | /v1/convai/agents/{agent_id}/link | Get Shareable Agent Link |
| POST | /v1/convai/agents/{agent_id}/avatar | Post Agent Avatar |
| GET | /v1/convai/agents | List Agents |
| GET | /v1/convai/agent/{agent_id}/knowledge-base/size | Returns The Size Of The Agent'S Knowledge Base |
| POST | /v1/convai/agent/{agent_id}/llm-usage/calculate | Calculate Expected Llm Usage For An Agent |
| POST | /v1/convai/agents/{agent_id}/duplicate | Duplicate Agent |
| POST | /v1/convai/agents/{agent_id}/simulate-conversation | Simulates A Conversation |
| POST | /v1/convai/agents/{agent_id}/simulate-conversation/stream | Simulates A Conversation (Stream) |
| POST | /v1/convai/agent-testing/create | Create Agent Response Test |
| GET | /v1/convai/agent-testing/{test_id} | Get Agent Response Test By Id |
| PUT | /v1/convai/agent-testing/{test_id} | Update Agent Response Test |
| DELETE | /v1/convai/agent-testing/{test_id} | Delete Agent Response Test |
| POST | /v1/convai/agent-testing/summaries | Get Agent Response Test Summaries By Ids |
| GET | /v1/convai/agent-testing | List Agent Response Tests |
| GET | /v1/convai/test-invocations | List Test Invocations |
| POST | /v1/convai/agents/{agent_id}/run-tests | Run Tests On The Agent |
| GET | /v1/convai/test-invocations/{test_invocation_id} | Get Test Invocation |
| POST | /v1/convai/test-invocations/{test_invocation_id}/resubmit | Resubmit Tests |
| GET | /v1/convai/conversations | Get Conversations |
| GET | /v1/convai/users | Get Conversation Users |
| GET | /v1/convai/conversations/{conversation_id} | Get Conversation Details |
| DELETE | /v1/convai/conversations/{conversation_id} | Delete Conversation |
| GET | /v1/convai/conversations/{conversation_id}/audio | Get Conversation Audio |
| POST | /v1/convai/conversations/{conversation_id}/feedback | Send Conversation Feedback |
| GET | /v1/convai/conversations/messages/text-search | Text Search Conversation Messages |
| GET | /v1/convai/conversations/messages/smart-search | Smart Search Conversation Messages |
| POST | /v1/convai/phone-numbers | Import Phone Number |
| GET | /v1/convai/phone-numbers | List Phone Numbers |
| GET | /v1/convai/phone-numbers/{phone_number_id} | Get Phone Number |
| DELETE | /v1/convai/phone-numbers/{phone_number_id} | Delete Phone Number |
| PATCH | /v1/convai/phone-numbers/{phone_number_id} | Update Phone Number |
| POST | /v1/convai/llm-usage/calculate | Calculate Expected Llm Usage |
| GET | /v1/convai/llm/list | List Available Llms |
| POST | /v1/convai/conversations/{conversation_id}/files | Upload File |
| DELETE | /v1/convai/conversations/{conversation_id}/files/{file_id} | Delete File Upload |
| GET | /v1/convai/analytics/live-count | Get Live Count |
| GET | /v1/convai/knowledge-base/summaries | Get Knowledge Base Summaries By Ids |
| POST | /v1/convai/knowledge-base | Add To Knowledge Base |
| GET | /v1/convai/knowledge-base | Get Knowledge Base List |
| POST | /v1/convai/knowledge-base/url | Create Url Document |
| POST | /v1/convai/knowledge-base/file | Create File Document |
| POST | /v1/convai/knowledge-base/text | Create Text Document |
| POST | /v1/convai/knowledge-base/folder | Create Folder |
| PATCH | /v1/convai/knowledge-base/{documentation_id} | Update Document |
| GET | /v1/convai/knowledge-base/{documentation_id} | Get Documentation From Knowledge Base |
| DELETE | /v1/convai/knowledge-base/{documentation_id} | Delete Knowledge Base Document Or Folder |
| POST | /v1/convai/knowledge-base/rag-index | Compute Rag Indexes In Batch |
| GET | /v1/convai/knowledge-base/rag-index | Get Rag Index Overview. |
| POST | /v1/convai/knowledge-base/{documentation_id}/rag-index | Compute Rag Index. |
| GET | /v1/convai/knowledge-base/{documentation_id}/rag-index | Get Rag Indexes Of The Specified Knowledgebase Document. |
| DELETE | /v1/convai/knowledge-base/{documentation_id}/rag-index/{rag_index_id} | Delete Rag Index. |
| GET | /v1/convai/knowledge-base/{documentation_id}/dependent-agents | Get Dependent Agents List |
| GET | /v1/convai/knowledge-base/{documentation_id}/content | Get Document Content |
| GET | /v1/convai/knowledge-base/{documentation_id}/source-file-url | Get Document Source File Url |
| GET | /v1/convai/knowledge-base/{documentation_id}/chunk/{chunk_id} | Get Documentation Chunk From Knowledge Base |
| POST | /v1/convai/knowledge-base/{document_id}/move | Move Entity To Folder |
| POST | /v1/convai/knowledge-base/bulk-move | Bulk Move Entities To Folder |
| POST | /v1/convai/tools | Add Tool |
| GET | /v1/convai/tools | Get Tools |
| GET | /v1/convai/tools/{tool_id} | Get Tool |
| PATCH | /v1/convai/tools/{tool_id} | Update Tool |
| DELETE | /v1/convai/tools/{tool_id} | Delete Tool |
| GET | /v1/convai/tools/{tool_id}/dependent-agents | Get Dependent Agents List |
| GET | /v1/convai/settings | Get Convai Settings |
| PATCH | /v1/convai/settings | Update Convai Settings |
| GET | /v1/convai/settings/dashboard | Get Convai Dashboard Settings |
| PATCH | /v1/convai/settings/dashboard | Update Convai Dashboard Settings |
| POST | /v1/convai/secrets | Create Convai Workspace Secret |
| GET | /v1/convai/secrets | Get Convai Workspace Secrets |
| DELETE | /v1/convai/secrets/{secret_id} | Delete Convai Workspace Secret |
| PATCH | /v1/convai/secrets/{secret_id} | Update Convai Workspace Secret |
| POST | /v1/convai/batch-calling/submit | Submit A Batch Call Request. |
| GET | /v1/convai/batch-calling/workspace | Get All Batch Calls For A Workspace. |
| GET | /v1/convai/batch-calling/{batch_id} | Get A Batch Call By Id. |
| DELETE | /v1/convai/batch-calling/{batch_id} | Delete A Batch Call. |
| POST | /v1/convai/batch-calling/{batch_id}/cancel | Cancel A Batch Call. |
| POST | /v1/convai/batch-calling/{batch_id}/retry | Retry A Batch Call. |
| POST | /v1/convai/sip-trunk/outbound-call | Handle An Outbound Call Via Sip Trunk |
| POST | /v1/convai/mcp-servers | Create Mcp Server |
| GET | /v1/convai/mcp-servers | List Mcp Servers |
| GET | /v1/convai/mcp-servers/{mcp_server_id} | Get Mcp Server |
| DELETE | /v1/convai/mcp-servers/{mcp_server_id} | Delete Mcp Server |
| PATCH | /v1/convai/mcp-servers/{mcp_server_id} | Update Mcp Server Configuration |
| GET | /v1/convai/mcp-servers/{mcp_server_id}/tools | List Mcp Server Tools |
| PATCH | /v1/convai/mcp-servers/{mcp_server_id}/approval-policy | Update Mcp Server Approval Policy |
| POST | /v1/convai/mcp-servers/{mcp_server_id}/tool-approvals | Create Mcp Server Tool Approval |
| DELETE | /v1/convai/mcp-servers/{mcp_server_id}/tool-approvals/{tool_name} | Delete Mcp Server Tool Approval |
| POST | /v1/convai/mcp-servers/{mcp_server_id}/tool-configs | Create Mcp Tool Configuration Override |
| GET | /v1/convai/mcp-servers/{mcp_server_id}/tool-configs/{tool_name} | Get Mcp Tool Configuration Override |
| PATCH | /v1/convai/mcp-servers/{mcp_server_id}/tool-configs/{tool_name} | Update Mcp Tool Configuration Override |
| DELETE | /v1/convai/mcp-servers/{mcp_server_id}/tool-configs/{tool_name} | Delete Mcp Tool Configuration Override |
| GET | /v1/convai/whatsapp-accounts/{phone_number_id} | Get Whatsapp Account |
| PATCH | /v1/convai/whatsapp-accounts/{phone_number_id} | Update Whatsapp Account |
| DELETE | /v1/convai/whatsapp-accounts/{phone_number_id} | Delete Whatsapp Account |
| GET | /v1/convai/whatsapp-accounts | List Whatsapp Accounts |
| POST | /v1/convai/agents/{agent_id}/branches | Create A New Branch |
| GET | /v1/convai/agents/{agent_id}/branches | List Agent Branches |
| GET | /v1/convai/agents/{agent_id}/branches/{branch_id} | Get Agent Branch |
| PATCH | /v1/convai/agents/{agent_id}/branches/{branch_id} | Update Agent Branch |
| POST | /v1/convai/agents/{agent_id}/branches/{source_branch_id}/merge | Merge A Branch Into A Target Branch |
| POST | /v1/convai/agents/{agent_id}/deployments | Create Or Update Deployments |
| POST | /v1/convai/agents/{agent_id}/drafts | Create Agent Draft |
| DELETE | /v1/convai/agents/{agent_id}/drafts | Delete Agent Draft |

### music
| Method | Path | Description |
|--------|------|-------------|
| POST | /v1/music/plan | Generate Composition Plan |
| POST | /v1/music | Compose Music |
| POST | /v1/music/detailed | Compose Music With A Detailed Response |
| POST | /v1/music/stream | Stream Composed Music |
| POST | /v1/music/upload | Upload Music |
| POST | /v1/music/stem-separation | Stem Separation |

### docs
| Method | Path | Description |
|--------|------|-------------|
| GET | /docs | Redirect To Mintlify |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search history?" -> GET /v1/history
- "Get history details?" -> GET /v1/history/{history_item_id}
- "Delete a history?" -> DELETE /v1/history/{history_item_id}
- "List all audio?" -> GET /v1/history/{history_item_id}/audio
- "Create a download?" -> POST /v1/history/download
- "Create a sound-generation?" -> POST /v1/sound-generation
- "Create a audio-isolation?" -> POST /v1/audio-isolation
- "Create a stream?" -> POST /v1/audio-isolation/stream
- "Delete a sample?" -> DELETE /v1/voices/{voice_id}/samples/{sample_id}
- "List all audio?" -> GET /v1/voices/{voice_id}/samples/{sample_id}/audio
- "Create a with-timestamp?" -> POST /v1/text-to-speech/{voice_id}/with-timestamps
- "Create a stream?" -> POST /v1/text-to-speech/{voice_id}/stream
- "Create a with-timestamp?" -> POST /v1/text-to-speech/{voice_id}/stream/with-timestamps
- "Create a text-to-dialogue?" -> POST /v1/text-to-dialogue
- "Create a stream?" -> POST /v1/text-to-dialogue/stream
- "Create a with-timestamp?" -> POST /v1/text-to-dialogue/stream/with-timestamps
- "Create a with-timestamp?" -> POST /v1/text-to-dialogue/with-timestamps
- "Create a stream?" -> POST /v1/speech-to-speech/{voice_id}/stream
- "Create a create-preview?" -> POST /v1/text-to-voice/create-previews
- "Create a text-to-voice?" -> POST /v1/text-to-voice
- "Create a design?" -> POST /v1/text-to-voice/design
- "Create a remix?" -> POST /v1/text-to-voice/{voice_id}/remix
- "List all stream?" -> GET /v1/text-to-voice/{generated_voice_id}/stream
- "List all subscription?" -> GET /v1/user/subscription
- "List all user?" -> GET /v1/user
- "List all voices?" -> GET /v1/voices
- "Search voices?" -> GET /v2/voices
- "List all default?" -> GET /v1/voices/settings/default
- "List all settings?" -> GET /v1/voices/{voice_id}/settings
- "Get voice details?" -> GET /v1/voices/{voice_id}
- "Delete a voice?" -> DELETE /v1/voices/{voice_id}
- "Create a edit?" -> POST /v1/voices/{voice_id}/settings/edit
- "Create a add?" -> POST /v1/voices/add
- "Create a edit?" -> POST /v1/voices/{voice_id}/edit
- "Create a podcast?" -> POST /v1/studio/podcasts
- "Create a pronunciation-dictionary?" -> POST /v1/studio/projects/{project_id}/pronunciation-dictionaries
- "List all projects?" -> GET /v1/studio/projects
- "Create a project?" -> POST /v1/studio/projects
- "Get project details?" -> GET /v1/studio/projects/{project_id}
- "Delete a project?" -> DELETE /v1/studio/projects/{project_id}
- "Create a content?" -> POST /v1/studio/projects/{project_id}/content
- "Create a convert?" -> POST /v1/studio/projects/{project_id}/convert
- "List all snapshots?" -> GET /v1/studio/projects/{project_id}/snapshots
- "Get snapshot details?" -> GET /v1/studio/projects/{project_id}/snapshots/{project_snapshot_id}
- "Create a stream?" -> POST /v1/studio/projects/{project_id}/snapshots/{project_snapshot_id}/stream
- "Create a archive?" -> POST /v1/studio/projects/{project_id}/snapshots/{project_snapshot_id}/archive
- "List all chapters?" -> GET /v1/studio/projects/{project_id}/chapters
- "Create a chapter?" -> POST /v1/studio/projects/{project_id}/chapters
- "Get chapter details?" -> GET /v1/studio/projects/{project_id}/chapters/{chapter_id}
- "Delete a chapter?" -> DELETE /v1/studio/projects/{project_id}/chapters/{chapter_id}
- "Create a convert?" -> POST /v1/studio/projects/{project_id}/chapters/{chapter_id}/convert
- "List all snapshots?" -> GET /v1/studio/projects/{project_id}/chapters/{chapter_id}/snapshots
- "Get snapshot details?" -> GET /v1/studio/projects/{project_id}/chapters/{chapter_id}/snapshots/{chapter_snapshot_id}
- "Create a stream?" -> POST /v1/studio/projects/{project_id}/chapters/{chapter_id}/snapshots/{chapter_snapshot_id}/stream
- "List all muted-tracks?" -> GET /v1/studio/projects/{project_id}/muted-tracks
- "Get resource details?" -> GET /v1/dubbing/resource/{dubbing_id}
- "Create a language?" -> POST /v1/dubbing/resource/{dubbing_id}/language
- "Create a segment?" -> POST /v1/dubbing/resource/{dubbing_id}/speaker/{speaker_id}/segment
- "Partially update a segment?" -> PATCH /v1/dubbing/resource/{dubbing_id}/segment/{segment_id}/{language}
- "Create a migrate-segment?" -> POST /v1/dubbing/resource/{dubbing_id}/migrate-segments
- "Delete a segment?" -> DELETE /v1/dubbing/resource/{dubbing_id}/segment/{segment_id}
- "Create a transcribe?" -> POST /v1/dubbing/resource/{dubbing_id}/transcribe
- "Create a translate?" -> POST /v1/dubbing/resource/{dubbing_id}/translate
- "Create a dub?" -> POST /v1/dubbing/resource/{dubbing_id}/dub
- "Partially update a speaker?" -> PATCH /v1/dubbing/resource/{dubbing_id}/speaker/{speaker_id}
- "Create a speaker?" -> POST /v1/dubbing/resource/{dubbing_id}/speaker
- "List all similar-voices?" -> GET /v1/dubbing/resource/{dubbing_id}/speaker/{speaker_id}/similar-voices
- "List all dubbing?" -> GET /v1/dubbing
- "Create a dubbing?" -> POST /v1/dubbing
- "Get dubbing details?" -> GET /v1/dubbing/{dubbing_id}
- "Delete a dubbing?" -> DELETE /v1/dubbing/{dubbing_id}
- "Get audio details?" -> GET /v1/dubbing/{dubbing_id}/audio/{language_code}
- "Get transcript details?" -> GET /v1/dubbing/{dubbing_id}/transcript/{language_code}
- "Get format details?" -> GET /v1/dubbing/{dubbing_id}/transcripts/{language_code}/format/{format_type}
- "List all models?" -> GET /v1/models
- "Create a audio-native?" -> POST /v1/audio-native
- "List all settings?" -> GET /v1/audio-native/{project_id}/settings
- "Create a content?" -> POST /v1/audio-native/{project_id}/content
- "Create a content?" -> POST /v1/audio-native/content
- "Search shared-voices?" -> GET /v1/shared-voices
- "Create a similar-voice?" -> POST /v1/similar-voices
- "List all character-stats?" -> GET /v1/usage/character-stats
- "Create a add-from-file?" -> POST /v1/pronunciation-dictionaries/add-from-file
- "Create a add-from-rule?" -> POST /v1/pronunciation-dictionaries/add-from-rules
- "Partially update a pronunciation-dictionary?" -> PATCH /v1/pronunciation-dictionaries/{pronunciation_dictionary_id}
- "Get pronunciation-dictionary details?" -> GET /v1/pronunciation-dictionaries/{pronunciation_dictionary_id}
- "Create a set-rule?" -> POST /v1/pronunciation-dictionaries/{pronunciation_dictionary_id}/set-rules
- "Create a add-rule?" -> POST /v1/pronunciation-dictionaries/{pronunciation_dictionary_id}/add-rules
- "Create a remove-rule?" -> POST /v1/pronunciation-dictionaries/{pronunciation_dictionary_id}/remove-rules
- "List all download?" -> GET /v1/pronunciation-dictionaries/{dictionary_id}/{version_id}/download
- "List all pronunciation-dictionaries?" -> GET /v1/pronunciation-dictionaries
- "List all api-keys?" -> GET /v1/service-accounts/{service_account_user_id}/api-keys
- "Create a api-key?" -> POST /v1/service-accounts/{service_account_user_id}/api-keys
- "Partially update a api-key?" -> PATCH /v1/service-accounts/{service_account_user_id}/api-keys/{api_key_id}
- "Delete a api-key?" -> DELETE /v1/service-accounts/{service_account_user_id}/api-keys/{api_key_id}
- "List all service-accounts?" -> GET /v1/service-accounts
- "List all search?" -> GET /v1/workspace/groups/search
- "Create a remove?" -> POST /v1/workspace/groups/{group_id}/members/remove
- "Create a member?" -> POST /v1/workspace/groups/{group_id}/members
- "Create a add?" -> POST /v1/workspace/invites/add
- "Create a add-bulk?" -> POST /v1/workspace/invites/add-bulk
- "Create a member?" -> POST /v1/workspace/members
- "Get resource details?" -> GET /v1/workspace/resources/{resource_id}
- "Create a share?" -> POST /v1/workspace/resources/{resource_id}/share
- "Create a unshare?" -> POST /v1/workspace/resources/{resource_id}/unshare
- "List all webhooks?" -> GET /v1/workspace/webhooks
- "Create a webhook?" -> POST /v1/workspace/webhooks
- "Partially update a webhook?" -> PATCH /v1/workspace/webhooks/{webhook_id}
- "Delete a webhook?" -> DELETE /v1/workspace/webhooks/{webhook_id}
- "Create a speech-to-text?" -> POST /v1/speech-to-text
- "Get transcript details?" -> GET /v1/speech-to-text/transcripts/{transcription_id}
- "Delete a transcript?" -> DELETE /v1/speech-to-text/transcripts/{transcription_id}
- "Create a forced-alignment?" -> POST /v1/forced-alignment
- "List all get-signed-url?" -> GET /v1/convai/conversation/get-signed-url
- "List all get_signed_url?" -> GET /v1/convai/conversation/get_signed_url
- "List all token?" -> GET /v1/convai/conversation/token
- "Create a outbound-call?" -> POST /v1/convai/twilio/outbound-call
- "Create a register-call?" -> POST /v1/convai/twilio/register-call
- "Create a outbound-call?" -> POST /v1/convai/whatsapp/outbound-call
- "Create a outbound-message?" -> POST /v1/convai/whatsapp/outbound-message
- "Create a create?" -> POST /v1/convai/agents/create
- "List all summaries?" -> GET /v1/convai/agents/summaries
- "Get agent details?" -> GET /v1/convai/agents/{agent_id}
- "Partially update a agent?" -> PATCH /v1/convai/agents/{agent_id}
- "Delete a agent?" -> DELETE /v1/convai/agents/{agent_id}
- "List all widget?" -> GET /v1/convai/agents/{agent_id}/widget
- "List all link?" -> GET /v1/convai/agents/{agent_id}/link
- "Create a avatar?" -> POST /v1/convai/agents/{agent_id}/avatar
- "Search agents?" -> GET /v1/convai/agents
- "List all size?" -> GET /v1/convai/agent/{agent_id}/knowledge-base/size
- "Create a calculate?" -> POST /v1/convai/agent/{agent_id}/llm-usage/calculate
- "Create a duplicate?" -> POST /v1/convai/agents/{agent_id}/duplicate
- "Create a simulate-conversation?" -> POST /v1/convai/agents/{agent_id}/simulate-conversation
- "Create a stream?" -> POST /v1/convai/agents/{agent_id}/simulate-conversation/stream
- "Create a create?" -> POST /v1/convai/agent-testing/create
- "Get agent-testing details?" -> GET /v1/convai/agent-testing/{test_id}
- "Update a agent-testing?" -> PUT /v1/convai/agent-testing/{test_id}
- "Delete a agent-testing?" -> DELETE /v1/convai/agent-testing/{test_id}
- "Create a summary?" -> POST /v1/convai/agent-testing/summaries
- "Search agent-testing?" -> GET /v1/convai/agent-testing
- "List all test-invocations?" -> GET /v1/convai/test-invocations
- "Create a run-test?" -> POST /v1/convai/agents/{agent_id}/run-tests
- "Get test-invocation details?" -> GET /v1/convai/test-invocations/{test_invocation_id}
- "Create a resubmit?" -> POST /v1/convai/test-invocations/{test_invocation_id}/resubmit
- "Search conversations?" -> GET /v1/convai/conversations
- "Search users?" -> GET /v1/convai/users
- "Get conversation details?" -> GET /v1/convai/conversations/{conversation_id}
- "Delete a conversation?" -> DELETE /v1/convai/conversations/{conversation_id}
- "List all audio?" -> GET /v1/convai/conversations/{conversation_id}/audio
- "Create a feedback?" -> POST /v1/convai/conversations/{conversation_id}/feedback
- "List all text-search?" -> GET /v1/convai/conversations/messages/text-search
- "List all smart-search?" -> GET /v1/convai/conversations/messages/smart-search
- "Create a phone-number?" -> POST /v1/convai/phone-numbers
- "List all phone-numbers?" -> GET /v1/convai/phone-numbers
- "Get phone-number details?" -> GET /v1/convai/phone-numbers/{phone_number_id}
- "Delete a phone-number?" -> DELETE /v1/convai/phone-numbers/{phone_number_id}
- "Partially update a phone-number?" -> PATCH /v1/convai/phone-numbers/{phone_number_id}
- "Create a calculate?" -> POST /v1/convai/llm-usage/calculate
- "List all list?" -> GET /v1/convai/llm/list
- "Create a file?" -> POST /v1/convai/conversations/{conversation_id}/files
- "Delete a file?" -> DELETE /v1/convai/conversations/{conversation_id}/files/{file_id}
- "List all live-count?" -> GET /v1/convai/analytics/live-count
- "List all summaries?" -> GET /v1/convai/knowledge-base/summaries
- "Create a knowledge-base?" -> POST /v1/convai/knowledge-base
- "Search knowledge-base?" -> GET /v1/convai/knowledge-base
- "Create a url?" -> POST /v1/convai/knowledge-base/url
- "Create a file?" -> POST /v1/convai/knowledge-base/file
- "Create a text?" -> POST /v1/convai/knowledge-base/text
- "Create a folder?" -> POST /v1/convai/knowledge-base/folder
- "Partially update a knowledge-base?" -> PATCH /v1/convai/knowledge-base/{documentation_id}
- "Get knowledge-base details?" -> GET /v1/convai/knowledge-base/{documentation_id}
- "Delete a knowledge-base?" -> DELETE /v1/convai/knowledge-base/{documentation_id}
- "Create a rag-index?" -> POST /v1/convai/knowledge-base/rag-index
- "List all rag-index?" -> GET /v1/convai/knowledge-base/rag-index
- "Create a rag-index?" -> POST /v1/convai/knowledge-base/{documentation_id}/rag-index
- "List all rag-index?" -> GET /v1/convai/knowledge-base/{documentation_id}/rag-index
- "Delete a rag-index?" -> DELETE /v1/convai/knowledge-base/{documentation_id}/rag-index/{rag_index_id}
- "List all dependent-agents?" -> GET /v1/convai/knowledge-base/{documentation_id}/dependent-agents
- "List all content?" -> GET /v1/convai/knowledge-base/{documentation_id}/content
- "List all source-file-url?" -> GET /v1/convai/knowledge-base/{documentation_id}/source-file-url
- "Get chunk details?" -> GET /v1/convai/knowledge-base/{documentation_id}/chunk/{chunk_id}
- "Create a move?" -> POST /v1/convai/knowledge-base/{document_id}/move
- "Create a bulk-move?" -> POST /v1/convai/knowledge-base/bulk-move
- "Create a tool?" -> POST /v1/convai/tools
- "Search tools?" -> GET /v1/convai/tools
- "Get tool details?" -> GET /v1/convai/tools/{tool_id}
- "Partially update a tool?" -> PATCH /v1/convai/tools/{tool_id}
- "Delete a tool?" -> DELETE /v1/convai/tools/{tool_id}
- "List all dependent-agents?" -> GET /v1/convai/tools/{tool_id}/dependent-agents
- "List all settings?" -> GET /v1/convai/settings
- "List all dashboard?" -> GET /v1/convai/settings/dashboard
- "Create a secret?" -> POST /v1/convai/secrets
- "List all secrets?" -> GET /v1/convai/secrets
- "Delete a secret?" -> DELETE /v1/convai/secrets/{secret_id}
- "Partially update a secret?" -> PATCH /v1/convai/secrets/{secret_id}
- "Create a submit?" -> POST /v1/convai/batch-calling/submit
- "List all workspace?" -> GET /v1/convai/batch-calling/workspace
- "Get batch-calling details?" -> GET /v1/convai/batch-calling/{batch_id}
- "Delete a batch-calling?" -> DELETE /v1/convai/batch-calling/{batch_id}
- "Create a cancel?" -> POST /v1/convai/batch-calling/{batch_id}/cancel
- "Create a retry?" -> POST /v1/convai/batch-calling/{batch_id}/retry
- "Create a outbound-call?" -> POST /v1/convai/sip-trunk/outbound-call
- "Create a mcp-server?" -> POST /v1/convai/mcp-servers
- "List all mcp-servers?" -> GET /v1/convai/mcp-servers
- "Get mcp-server details?" -> GET /v1/convai/mcp-servers/{mcp_server_id}
- "Delete a mcp-server?" -> DELETE /v1/convai/mcp-servers/{mcp_server_id}
- "Partially update a mcp-server?" -> PATCH /v1/convai/mcp-servers/{mcp_server_id}
- "List all tools?" -> GET /v1/convai/mcp-servers/{mcp_server_id}/tools
- "Create a tool-approval?" -> POST /v1/convai/mcp-servers/{mcp_server_id}/tool-approvals
- "Delete a tool-approval?" -> DELETE /v1/convai/mcp-servers/{mcp_server_id}/tool-approvals/{tool_name}
- "Create a tool-config?" -> POST /v1/convai/mcp-servers/{mcp_server_id}/tool-configs
- "Get tool-config details?" -> GET /v1/convai/mcp-servers/{mcp_server_id}/tool-configs/{tool_name}
- "Partially update a tool-config?" -> PATCH /v1/convai/mcp-servers/{mcp_server_id}/tool-configs/{tool_name}
- "Delete a tool-config?" -> DELETE /v1/convai/mcp-servers/{mcp_server_id}/tool-configs/{tool_name}
- "Get whatsapp-account details?" -> GET /v1/convai/whatsapp-accounts/{phone_number_id}
- "Partially update a whatsapp-account?" -> PATCH /v1/convai/whatsapp-accounts/{phone_number_id}
- "Delete a whatsapp-account?" -> DELETE /v1/convai/whatsapp-accounts/{phone_number_id}
- "List all whatsapp-accounts?" -> GET /v1/convai/whatsapp-accounts
- "Create a branche?" -> POST /v1/convai/agents/{agent_id}/branches
- "List all branches?" -> GET /v1/convai/agents/{agent_id}/branches
- "Get branche details?" -> GET /v1/convai/agents/{agent_id}/branches/{branch_id}
- "Partially update a branche?" -> PATCH /v1/convai/agents/{agent_id}/branches/{branch_id}
- "Create a merge?" -> POST /v1/convai/agents/{agent_id}/branches/{source_branch_id}/merge
- "Create a deployment?" -> POST /v1/convai/agents/{agent_id}/deployments
- "Create a draft?" -> POST /v1/convai/agents/{agent_id}/drafts
- "Create a plan?" -> POST /v1/music/plan
- "Create a music?" -> POST /v1/music
- "Create a detailed?" -> POST /v1/music/detailed
- "Create a stream?" -> POST /v1/music/stream
- "Create a upload?" -> POST /v1/music/upload
- "Create a stem-separation?" -> POST /v1/music/stem-separation
- "Create a pvc?" -> POST /v1/voices/pvc
- "Create a sample?" -> POST /v1/voices/pvc/{voice_id}/samples
- "Delete a sample?" -> DELETE /v1/voices/pvc/{voice_id}/samples/{sample_id}
- "List all audio?" -> GET /v1/voices/pvc/{voice_id}/samples/{sample_id}/audio
- "List all waveform?" -> GET /v1/voices/pvc/{voice_id}/samples/{sample_id}/waveform
- "List all speakers?" -> GET /v1/voices/pvc/{voice_id}/samples/{sample_id}/speakers
- "Create a separate-speaker?" -> POST /v1/voices/pvc/{voice_id}/samples/{sample_id}/separate-speakers
- "List all audio?" -> GET /v1/voices/pvc/{voice_id}/samples/{sample_id}/speakers/{speaker_id}/audio
- "List all captcha?" -> GET /v1/voices/pvc/{voice_id}/captcha
- "Create a captcha?" -> POST /v1/voices/pvc/{voice_id}/captcha
- "Create a train?" -> POST /v1/voices/pvc/{voice_id}/train
- "Create a verification?" -> POST /v1/voices/pvc/{voice_id}/verification
- "List all docs?" -> GET /docs
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
