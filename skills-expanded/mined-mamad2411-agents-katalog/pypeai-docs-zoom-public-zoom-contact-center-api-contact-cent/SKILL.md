# Assign queue agents

POST {{baseUrl}}/contact_center/queues/:queueId/agents


<p>
Add agents to a queue. 
</p>



<p>

<strong>
Scopes:
</strong>
 
<code>
contact_center_queue:write:admin
</code>

</p>



<p>

<strong>

<a href="https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits">
Rate Limit Label
</a>
:
</strong>
 
<code>
Medium
</code>

</p>





### Request Body
```
{&quot;user_ids&quot;=&gt;[&quot;&lt;string&gt;&quot;, &quot;&lt;string&gt;&quot;]}
```

### HEADERS
| Key | Datatype | Required | Description |
| `Content-Type` | string |  |  |
| `Accept` | string |  |  |


### RESPONSES

**status**: `Created`
```
{&quot;agents&quot;:[{&quot;user_id&quot;:&quot;\u003cstring\u003e&quot;,&quot;display_name&quot;:&quot;\u003cstring\u003e&quot;,&quot;user_email&quot;:&quot;\u003cemail\u003e&quot;,&quot;role_id&quot;:&quot;\u003cstring\u003e&quot;,&quot;role_name&quot;:&quot;\u003cstring\u003e&quot;,&quot;status_id&quot;:&quot;\u003cstring\u003e&quot;,&quot;status_name&quot;:&quot;Offline&quot;,&quot;user_access&quot;:&quot;inactive&quot;,&quot;opt_in_out_status&quot;:0},{&quot;user_id&quot;:&quot;\u003cstring\u003e&quot;,&quot;display_name&quot;:&quot;\u003cstring\u003e&quot;,&quot;user_email&quot;:&quot;\u003cemail\u003e&quot;,&quot;role_id&quot;:&quot;\u003cstring\u003e&quot;,&quot;role_name&quot;:&quot;\u003cstring\u003e&quot;,&quot;status_id&quot;:&quot;\u003cstring\u003e&quot;,&quot;status_name&quot;:&quot;Not Ready&quot;,&quot;user_access&quot;:&quot;active&quot;,&quot;opt_in_out_status&quot;:0}]}
```