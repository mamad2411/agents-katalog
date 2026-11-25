<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hakivvi
description: CTF writeups and security challenges by hakivvi.
---

# Writeups by hakivvi

Source repository: `/repos/hakivvi`

## Repository Index

- CVE-2021-3560/README.md
- CVE-2022-29464/README.md

## Writeup Content


### File: CVE-2021-3560/README.md

# CVE-2021-3560
a reliable C based exploit for CVE-2021-3560.

# Summary:
Yestreday i stumbled upon this [blog post](https://github.blog/2021-06-10-privilege-escalation-polkit-root-on-linux-with-bug/) by Kevin Backhouse (discovered this vulnerability), i tried the bash commands provided in the blogpost and to my surpise it worked on my Kali Linux box!

CVE-2021-3560 is an authentication bypass on polkit, which allows an unprivileged user to call privileged methods using DBus, the PoC exploits this bug to call 2 privileged methods provided by accountsservice (`CreateUser` and `SetPassword`), which allows us to create a priviliged user then setting a password to it.

polkit checks if the caller is authorized to call such method, it does so by checking first the user id of the caller, if it is zero then the caller is assumed to be root and the action is allowed without asking for authentication, otherwise it asks for the password of the user.

`polkit_system_bus_name_get_creds_sync()` function invokes to 2 methods to get the UID and PID of the caller [`GetConnectionUnixUser`](https://gitlab.freedesktop.org/polkit/polkit/-/blob/ff4c2144f0fb1325275887d9e254117fcd8a1b52/src/polkit/polkitsystembusname.c#L410) and [`GetConnectionUnixProcessID`](https://gitlab.freedesktop.org/polkit/polkit/-/blob/ff4c2144f0fb1325275887d9e254117fcd8a1b52/src/polkit/polkitsystembusname.c#L422), the result of this calls is written to the `data` struct of type `AsyncGetBusNameCredsData` (this struct is [intialized to 0](https://gitlab.freedesktop.org/polkit/polkit/-/blob/ff4c2144f0fb1325275887d9e254117fcd8a1b52/src/polkit/polkitsystembusname.c#L395)) by the callback function `on_retrieved_unix_uid_pid()`, and `polkit_system_bus_name_get_creds_sync()` blocks while waiting for the callback function to set an error or the UID and PID.

```C
static gboolean
polkit_system_bus_name_get_creds_sync (PolkitSystemBusName           *system_bus_name,
				       guint32                       *out_uid,
				       guint32                       *out_pid,
				       GCancellable                  *cancellable,
				       GError                       **error)
{
  gboolean ret = FALSE;
  AsyncGetBusNameCredsData data = { 0, }; // intialize to 0
  GDBusConnection *connection = NULL;
  GMainContext *tmp_context = NULL;

  connection = g_bus_get_sync (G_BUS_TYPE_SYSTEM, cancellable, error);
  if (connection == NULL)
    goto out;

  data.error = error;

  tmp_context = g_main_context_new ();
  g_main_context_push_thread_default (tmp_context);

  g_dbus_connection_call (connection,
			  "org.freedesktop.DBus",       /* name */
			  "/org/freedesktop/DBus",      /* object path */
			  "org.freedesktop.DBus",       /* interface name */
			  "GetConnectionUnixUser",      /* method */
			  g_variant_new ("(s)", system_bus_name->name),
			  G_VARIANT_TYPE ("(u)"),
			  G_DBUS_CALL_FLAGS_NONE,
			  -1,
			  cancellable,
			  on_retrieved_unix_uid_pid, // callback funtion
			  &data); // data is passed to the callback function along with the reply from the method
  g_dbus_connection_call (connection,
			  "org.freedesktop.DBus",       /* name */
			  "/org/freedesktop/DBus",      /* object path */
			  "org.freedesktop.DBus",       /* interface name */
			  "GetConnectionUnixProcessID", /* method */
			  g_variant_new ("(s)", system_bus_name->name),
			  G_VARIANT_TYPE ("(u)"),
			  G_DBUS_CALL_FLAGS_NONE,
			  -1,
			  cancellable,
			  on_retrieved_unix_uid_pid, // callback funtion
			  &data); // data is passed to the callback function along with the reply from the method

  while (!((data.retrieved_uid && data.retrieved_pid) || data.caught_error)) // block while on_retrieved_unix_uid_pid() is not called yet
    g_main_context_iteration (tmp_context, TRUE);

```

the callback function [`on_retrieved_unix_uid_pid()`](https://gitlab.freedesktop.org/polkit/polkit/-/blob/ff4c2144f0fb1325275887d9e254117fcd8a1b52/src/polkit/polkitsystembusname.c#L355) is invoked after each method call to retirive the reply (UID and PID) or set an error, this function calls `g_dbus_connection_call_finish()` to retrive the reply if an [error is occured](https://gitlab.freedesktop.org/polkit/polkit/-/blob/ff4c2144f0fb1325275887d9e254117fcd8a1b52/src/polkit/polkitsystembusname.c#L364) then it sets `data.caught_error` to TRUE and returns (`data.uid` and `data.pid` are still set 0). otherwise it assign the retrieved value (UID or PID) to `data.uid` or `data.pid` (depends on what value is retrieved) then returns.

```C
static void
on_retrieved_unix_uid_pid (GObject              *src, // connection
			   GAsyncResult         *res, // Async result object
			   gpointer              user_data) // data paramter passed from previous function
{
  AsyncGetBusNameCredsData *data = user_data;
  GVariant *v;

  v = g_dbus_connection_call_finish ((GDBusConnection*)src, res,
				     data->caught_error ? NULL : data->error); // finish and get the reply
  if (!v) // error ??
    {
      data->caught_error = TRUE;
    }
  else
    {
      guint32 value;
      g_variant_get (v, "(u)", &value); // unpack the reply, get UINT32 (u)
      g_variant_unref (v);
      if (!data->retrieved_uid) // GetConnectionUnixUser method
	{
	  data->retrieved_uid = TRUE;
	  data->uid = value;
	}
      else
	{
	  g_assert (!data->retrieved_pid); // GetConnectionUnixProcessID method
	  data->retrieved_pid = TRUE;
	  data->pid = value;
	}
    }
}

```

`GetConnectionUnixUser` and `GetConnectionUnixProcessID` methods will return the UID and PID if found (caller process is still connected to the bus), or an error if an error occured (e.g: caller process killed).

once `data.uid` and `data.pid` are set or `data.caught_error` is set the function `polkit_system_bus_name_get_creds_sync()` will continue and here where the vulnerabilty exists, `polkit_system_bus_name_get_creds_sync()` does not return an error if `data.caught_error` is set, instead it set whatever value is in `data.uid` to `out_uid` and [returns TRUE](https://gitlab.freedesktop.org/polkit/polkit/-/blob/ff4c2144f0fb1325275887d9e254117fcd8a1b52/src/polkit/polkitsystembusname.c#L442) (even if `data.caught_error` is set). `out_pid` is a pointer to a `guint32` variable passed to `polkit_system_bus_name_get_creds_sync()` when called by `polkit_system_bus_name_get_user_sync()`:

```C
static gboolean
polkit_system_bus_name_get_creds_sync (PolkitSystemBusName           *system_bus_name,
				       guint32                       *out_uid, // pointer
				       guint32                       *out_pid, // NULL
				       GCancellable                  *cancellable,
				       GError                       **error)
{

  [snip]
  
  while (!((data.retrieved_uid && data.retrieved_pid) || data.caught_error)) // wait for the callback function to handle reply
    g_main_context_iteration (tmp_context, TRUE);

  if (out_uid) // TRUE
    *out_uid = data.uid; // set it even if there is an error [!]
  if (out_pid) // FALSE
    *out_pid = data.pid; // set it even if there is an error [!]
  ret = TRUE; // return TRUE even if there is an error [!]
 out:
  if (tmp_context)
    {
      g_main_context_pop_thread_default (tmp_context);
      g_main_context_unref (tmp_context);
    }
  if (connection != NULL)
    g_object_unref (connection);
  return ret;

```

**exploitation:**

if the a process A calls a priviliged method using DBus, then polkit will check the UID of the caller, if process A exits imidiatly after it sends the message, then the methods `GetConnectionUnixUser` and `GetConnectionUnixProcessID` will return an error because the caller process does not exist anymore. the callback function `on_retrieved_unix_uid_pid()` will set `data.caught_error` to TRUE, `data.uid` and `data.pid` will remain unchanged (which means they will be both set to 0 as the data struct is intiailized to 0). the function `polkit_system_bus_name_get_creds_sync()` will continue the execution and sets `out_uid` to `data.uid` (0), and return TRUE.


a couple of function will keep returning the fake UID (0), until `polkit_backend_session_monitor_get_user_for_subject()` returns `user_of_subject` (built from the fake UID) to `check_authorization_sync()` function, which checks if the UID is root by calling [`identity_is_root_user(user_of_subject)`](https://gitlab.freedesktop.org/polkit/polkit/-/blob/ff4c2144f0fb1325275887d9e254117fcd8a1b52/src/polkitbackend/polkitbackendinteractiveauthority.c#L1128) which will return TRUE and process A will be [authorized](https://gitlab.freedesktop.org/polkit/polkit/-/blob/ff4c2144f0fb1325275887d9e254117fcd8a1b52/src/polkitbackend/polkitbackendinteractiveauthority.c#L1130).

```C
static PolkitAuthorizationResult *
check_authorization_sync (PolkitBackendAuthority         *authority,
                          PolkitSubject                  *caller,
                          PolkitSubject                  *subject,
                          const gchar                    *action_id,
                          PolkitDetails                  *details,
                          PolkitCheckAuthorizationFlags   flags,
                          PolkitImplicitAuthorization    *out_implicit_authorization,
                          gboolean                        checking_imply,
                          GError                        **error)
{

  
  [snip]

  user_of_subject = polkit_backend_session_monitor_get_user_for_subject (priv->session_monitor,
                                                                         subject, NULL,
                                                                         error);
  if (user_of_subject == NULL) // false
      goto out;

  /* special case: uid 0, root, is _always_ authorized for anything */
  if (identity_is_root_user (user_of_subject)) // true
    {
      result = polkit_authorization_result_new (TRUE, FALSE, NULL); // authorize the caller
      goto out;
    }

  [snip]
 
```

# PoC:
I decided to write a PoC using dbus C API, i didn't use `sleep()` while waiting for the message to be sent to the target service, instead, DBus functions provide a timeout paramter, so by (ab)using this parameter we can force the function to return just after it sends the message, then killing the process, this will allow us to exploit the vulnerability on polkit and bypass the authentication. refer to this [blog post](https://github.blog/2021-06-10-privilege-escalation-polkit-root-on-linux-with-bug/) for the technical details.

# run:
1. compile the exploit:

```
user@host: gcc -Wall exploit.c -o exploit $(pkg-config --libs --cflags dbus-1)
```
2. run the exploit:

```
user@host: ./exploit
```


- Output:
```
user@host:~/CVE-2021-3560-testing$ gcc -Wall exploit.c -o exploit $(pkg-config --libs --cflags dbus-1)
user@host:~/CVE-2021-3560-testing$ ./exploit
[*] creating "pwned-1624301069" user ...
[!] user has been created!
[*] user: pwned-1624301069, uid: 1007
[*] setting an empty password for "pwned-1624301069" user..
[*] an empty password has been set for "pwned-1624301069" user!
[!] run: "sudo su root" as "pwned-1624301069" user to get root
┌──(pwned-1624301069㉿host)-[/home/user/CVE-2021-3560-testing]
└─$ sudo su root

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

root@host:/home/user/CVE-2021-3560-testing# id
uid=0(root) gid=0(root) groups=0(root)
```




### File: CVE-2022-29464/README.md

# CVE-2022-29464
WSO2 RCE (CVE-2022-29464) exploit and writeup.
# Details
[CVE-2022-29464](https://docs.wso2.com/display/Security/Security+Advisory+WSO2-2021-1738) is critical vulnerability on WSO2 discovered by [Orange Tsai](https://twitter.com/orange_8361). the vulnerability is an unauthenticated unrestricted arbitrary file upload which allows unauthenticated attackers to gain RCE on WSO2 servers via uploading malicious JSP files. 

the vulerable upload route is `/fileupload` which is handled by [`FileUploadServlet`](https://github.com/wso2/carbon-kernel/blob/4.4.x/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/FileUploadServlet.java) servlet. and it is unprotected route by IAM as we can see in the  `indentity.xml` configuration file:
```xml
<Resource context="(.*)/fileupload(.*)" secured="false" http-method="all"/>
```
And also unprotected by the default login measure, `handleSecurity()` is the function responsible for securing the different routes served by WSO2 and provides a mechanism for performing security checks on the received HTTP requests, `handleSecurity()` will call `CarbonUILoginUtil.handleLoginPageRequest()` and based on its return value it will be decided to allow or deny access to the requested URI:
```java
    public boolean handleSecurity(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
	[snipped]
        if ((val = CarbonUILoginUtil.handleLoginPageRequest(requestedURI, request, response,
                authenticated, context, indexPageURL)) != CarbonUILoginUtil.CONTINUE) {
            if (val == CarbonUILoginUtil.RETURN_TRUE) {
                return true;
            } else {
                return false;
            }
        }
	[snipped]
    }
```
`CarbonUILoginUtil.handleLoginPageRequest()` returns `CarbonUILoginUtil.RETURN_TRUE` when the route is `/fileupload`:
```java
    protected static int handleLoginPageRequest(String requestedURI, HttpServletRequest request,
            HttpServletResponse response, boolean authenticated, String context, String indexPageURL)
            throws IOException {
        boolean isTryIt = requestedURI.indexOf("admin/jsp/WSRequestXSSproxy_ajaxprocessor.jsp") > -1;
        boolean isFileDownload = requestedURI.endsWith("/filedownload");
        if ((requestedURI.indexOf("login.jsp") > -1
                || requestedURI.indexOf("login_ajaxprocessor.jsp") > -1
                || requestedURI.indexOf("admin/layout/template.jsp") > -1
                || isFileDownload
                || requestedURI.endsWith("/fileupload")
                || requestedURI.indexOf("/fileupload/") > -1
                || requestedURI.indexOf("login_action.jsp") > -1
                || isTryIt
                || requestedURI.indexOf("tryit/JAXRSRequestXSSproxy_ajaxprocessor.jsp") > -1)
                && !requestedURI.contains(";")) {

            if ((requestedURI.indexOf("login.jsp") > -1
                    || requestedURI.indexOf("login_ajaxprocessor.jsp") > -1 || requestedURI
                    .indexOf("login_action.jsp") > -1) && authenticated) {
                [snipped]
            } else if ((isTryIt || isFileDownload) && !authenticated) {
                [snipped]
            } else if (requestedURI.indexOf("login_action.jsp") > -1 && !authenticated) {
                [snipped]
            } else {
				if (log.isDebugEnabled()) {
					log.debug("Skipping security checks for " + requestedURI);
				}
                return RETURN_TRUE;
            }
        }

        return CONTINUE;
    }
```
with `CarbonUILoginUtil.handleLoginPageRequest()` returning `CarbonUILoginUtil.RETURN_TRUE`, `handleSecurity()` will return `true`, the access will be then granted to `/fileupload` without authentication.

the `FileUploadServlet` servlet and upon [`init()`](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/FileUploadServlet.java#L71) and through a series of method calls loads eventually from the `carbon.xml` configuration file multiple upload file formats/actions along with the object which hanldes every format.
```java
    public void init(ServletConfig servletConfig) throws ServletException {
        this.servletConfig = servletConfig;
        try {
            fileUploadExecutorManager = new FileUploadExecutorManager(bundleContext, configContext, webContext);
            //Registering FileUploadExecutor Manager as an OSGi service
            bundleContext.registerService(FileUploadExecutorManager.class.getName(), fileUploadExecutorManager, null);
        } catch (CarbonException e) {
            log.error("Exception occurred while trying to initialize FileUploadServlet", e);
            throw new ServletException(e);
        }
    }
```
the [`FileUploadExecutorManager`](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/fileupload/FileUploadExecutorManager.java#L67) class constructor is as follows:
```java
    public FileUploadExecutorManager(BundleContext bundleContext,
                                     ConfigurationContext configCtx,
                                     String webContext) throws CarbonException {
        this.bundleContext = bundleContext;
        this.configContext = configCtx;
        this.webContext = webContext;
        this.loadExecutorMap();
    }
```
the constructor calls the private method [`loadExecutorMap()`](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/fileupload/FileUploadExecutorManager.java#L131) which is where the configuration loading is done:
```java
    private void loadExecutorMap() throws CarbonException {
        [snipped]
                try {
            documentElement = XMLUtils.toOM(serverConfiguration.getDocumentElement());
        } catch (Exception e) {
            String msg = "Unable to read Server Configuration.";
            log.error(msg);
            throw new CarbonException(msg, e);
        }
        [snipped]
        OMElement fileUploadConfigElement =
                documentElement.getFirstChildWithName(
                        new QName(ServerConstants.CARBON_SERVER_XML_NAMESPACE, "FileUploadConfig"));
        for (Iterator iterator = fileUploadConfigElement.getChildElements(); iterator.hasNext();) {
            OMElement mapppingElement = (OMElement) iterator.next();
            if (mapppingElement.getLocalName().equalsIgnoreCase("Mapping")) {
                OMElement actionsElement =
                        mapppingElement.getFirstChildWithName(
                                new QName(ServerConstants.CARBON_SERVER_XML_NAMESPACE, "Actions"));
                String confPath = System.getProperty(CarbonBaseConstants.CARBON_CONFIG_DIR_PATH);
        [snipped]
```
the file upload formats configurations is within the `FileUploadConfig` namespace in the XML configuration file, this is the default configuration:
```xml
    <FileUploadConfig>
        <!--
           The total file upload size limit in MB
        -->
        <TotalFileSizeLimit>100</TotalFileSizeLimit>

        <Mapping>
            <Actions>
                <Action>keystore</Action>
                <Action>certificate</Action>
                <Action>*</Action>
            </Actions>
            <Class>org.wso2.carbon.ui.transports.fileupload.AnyFileUploadExecutor</Class>
        </Mapping>

        <Mapping>
            <Actions>
                <Action>jarZip</Action>
            </Actions>
            <Class>org.wso2.carbon.ui.transports.fileupload.JarZipUploadExecutor</Class>
        </Mapping>
        <Mapping>
            <Actions>
                <Action>dbs</Action>
            </Actions>
            <Class>org.wso2.carbon.ui.transports.fileupload.DBSFileUploadExecutor</Class>
        </Mapping>
        <Mapping>
            <Actions>
                <Action>tools</Action>
            </Actions>
            <Class>org.wso2.carbon.ui.transports.fileupload.ToolsFileUploadExecutor</Class>
        </Mapping>
        <Mapping>
            <Actions>
                <Action>toolsAny</Action>
            </Actions>
            <Class>org.wso2.carbon.ui.transports.fileupload.ToolsAnyFileUploadExecutor</Class>
        </Mapping>
    </FileUploadConfig>
```
the `loadExecutorMap()` method creates and fills a `HashMap` of `<Action, Class>` with the Actions and the Classes extracted from the config file. which will be later used to choose which class to use to handle properly a given format/action.

Later on when the `/fileupload` route recieves a POST request the [`doPost()`](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/FileUploadServlet.java#L53) method of the servlet will be called. the method just forwards the request and response object to `execute()` method of `fileUploadExecutorManager` which was intitialized on `init()`
```java
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response) throws ServletException, IOException {

        try {
            fileUploadExecutorManager.execute(request, response);
        } catch (Exception e) {
            String msg = "File upload failed ";
            log.error(msg, e);
            throw new ServletException(e);
        }
    }
```
the `execute()` method, splits the request url just after the `fileupload/` string, which means it extacts whatever is after the `/fileupload/` in the request URL and it assignes is it to `actionString`.
```java
    public boolean execute(HttpServletRequest request,
                           HttpServletResponse response) throws IOException {

        HttpSession session = request.getSession();
        String cookie = (String) session.getAttribute(ServerConstants.ADMIN_SERVICE_COOKIE);
        request.setAttribute(CarbonConstants.ADMIN_SERVICE_COOKIE, cookie);
        request.setAttribute(CarbonConstants.WEB_CONTEXT, webContext);
        request.setAttribute(CarbonConstants.SERVER_URL,
                             CarbonUIUtil.getServerURL(request.getSession().getServletContext(),
                                                       request.getSession()));


        String requestURI = request.getRequestURI();

        //TODO - fileupload is hardcoded
        int indexToSplit = requestURI.indexOf("fileupload/") + "fileupload/".length();
        String actionString = requestURI.substring(indexToSplit);

        // Register execution handlers
        FileUploadExecutionHandlerManager execHandlerManager =
                new FileUploadExecutionHandlerManager();
        CarbonXmlFileUploadExecHandler carbonXmlExecHandler =
                new CarbonXmlFileUploadExecHandler(request, response, actionString);
        execHandlerManager.addExecHandler(carbonXmlExecHandler);
        OSGiFileUploadExecHandler osgiExecHandler =
                new OSGiFileUploadExecHandler(request, response);
        execHandlerManager.addExecHandler(osgiExecHandler);
        AnyFileUploadExecHandler anyFileExecHandler =
                new AnyFileUploadExecHandler(request, response);
        execHandlerManager.addExecHandler(anyFileExecHandler);
        execHandlerManager.startExec();
        return true;
    }
```
the `actionString` is passed to `CarbonXmlFileUploadExecHandler` class constructor along with `request` and `response`:
```java
        private CarbonXmlFileUploadExecHandler(HttpServletRequest request,
                                               HttpServletResponse response,
                                               String actionString) {
            this.request = request;
            this.response = response;
            this.actionString = actionString;
        }
```
the constructor will save them to its properties.

after that `carbonXmlExecHandler` object along with other objects will be added to [`execHandlerManager`](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/fileupload/FileUploadExecutorManager.java#L298) using `addExecHandler()` method.
```java
        public void addExecHandler(FileUploadExecutionHandler handler) {
            if (prevHandler != null) {
                prevHandler.setNext(handler);
            } else {
                firstHandler = handler;
            }
            prevHandler = handler;
        }
```
then `execHandlerManager.startExec()` is called:
```java
        public void startExec() throws IOException {
            firstHandler.execute();
        }
```
`startExec()` calls [`execute()`](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/fileupload/FileUploadExecutorManager.java#L430) of the first object added which is `CarbonXmlFileUploadExecHandler`:
```java
        public void execute() throws IOException {
            boolean foundExecutor = false;
            for (String key : executorMap.keySet()) {
                if (key.equals(actionString)) {
                    AbstractFileUploadExecutor obj = executorMap.get(key);
                    foundExecutor = true;
                    obj.executeGeneric(request, response, configContext);
                    break;
                }
            }
            if (!foundExecutor) {
                next();
            }
        }
```
[`execute()`](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/fileupload/FileUploadExecutorManager.java#L430) loops trough the `HashMap` of `<Action, Class>` created earlier and finds the Action (key) which is equal to `actionString`, if found the `executeGeneric()` method of the object associated with that Action will be called.

to revise the default configuration has 7 actions which are:
* `keystore`, `certificate`, `*` handled by `org.wso2.carbon.ui.transports.fileupload.AnyFileUploadExecutor`
* `jarZip` handled by `org.wso2.carbon.ui.transports.fileupload.JarZipUploadExecutor`
* `dbs` handled by `org.wso2.carbon.ui.transports.fileupload.DBSFileUploadExecutor`
* `tools` handled by `org.wso2.carbon.ui.transports.fileupload.ToolsFileUploadExecutor`
* `toolsAny` handled by `org.wso2.carbon.ui.transports.fileupload.ToolsAnyFileUploadExecutor`

each of these objects does handle the upload differently some of them accepts specific extensions. 

the first one i found vulnerable to arbitraty file write was `toolsAny` ([`ToolsAnyFileUploadExecutor`](https://github.com/wso2/carbon-kernel/blob/4.4.x/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/fileupload/ToolsAnyFileUploadExecutor.java)).
`ToolsAnyFileUploadExecutor` does not have a `executeGeneric()` method but it extends [`AbstractFileUploadExecutor`](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/fileupload/AbstractFileUploadExecutor.java#L61) which does have a [`executeGeneric()`](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/fileupload/AbstractFileUploadExecutor.java#L97) method:
```java
    boolean executeGeneric(HttpServletRequest request,
                           HttpServletResponse response,
                           ConfigurationContext configurationContext) throws IOException {//,
        //    CarbonException {
        this.configurationContext = configurationContext;
        try {
            parseRequest(request);
            return execute(request, response);
        } catch (FileUploadFailedException e) {
            sendErrorRedirect(request, response, e);
        } catch (FileSizeLimitExceededException e) {
            sendErrorRedirect(request, response, e);
        } catch (CarbonException e) {
            sendErrorRedirect(request, response, e);
        }
        return false;
    }
```
`executeGeneric()` calls first `parseRequest()` with the request object as a parameter:
```java
    protected void parseRequest(HttpServletRequest request) throws FileUploadFailedException,
                                                                 FileSizeLimitExceededException {
        fileItemsMap.set(new HashMap<String, ArrayList<FileItemData>>());
        formFieldsMap.set(new HashMap<String, ArrayList<String>>());

        ServletRequestContext servletRequestContext = new ServletRequestContext(request);
        boolean isMultipart = ServletFileUpload.isMultipartContent(servletRequestContext);
        Long totalFileSize = 0L;

        if (isMultipart) {

            List items;
            try {
                items = parseRequest(servletRequestContext);
            } catch (FileUploadException e) {
                String msg = "File upload failed";
                log.error(msg, e);
                throw new FileUploadFailedException(msg, e);
            }
            boolean multiItems = false;
            if (items.size() > 1) {
                multiItems = true;
            }

            // Add the uploaded items to the corresponding maps.
            for (Iterator iter = items.iterator(); iter.hasNext();) {
                FileItem item = (FileItem) iter.next();
                String fieldName = item.getFieldName().trim();
                if (item.isFormField()) {
                    if (formFieldsMap.get().get(fieldName) == null) {
                        formFieldsMap.get().put(fieldName, new ArrayList<String>());
                    }
                    try {
                        formFieldsMap.get().get(fieldName).add(new String(item.get(), "UTF-8"));
                    } catch (UnsupportedEncodingException ignore) {
                    }
                } else {
                    String fileName = item.getName();
                    if ((fileName == null || fileName.length() == 0) && multiItems) {
                        continue;
                    }
                    if (fileItemsMap.get().get(fieldName) == null) {
                        fileItemsMap.get().put(fieldName, new ArrayList<FileItemData>());
                    }
                    totalFileSize += item.getSize();
                    if (totalFileSize < totalFileUploadSizeLimit) {
                        fileItemsMap.get().get(fieldName).add(new FileItemData(item));
                    } else {
                        throw new FileSizeLimitExceededException(getFileSizeLimit() / 1024 / 1024);
                    }
                }
            }
        }
    }
```
it first assures that the POST request is a multipart POST request, and then extarcts the uploaded files, assures that the POST request contains at least on uploaded file and validates it against the maximum file size.

after returning from `parseRequest()`, `executeGeneric()` will call now the `execute()` method which is [overrode](https://github.com/wso2/carbon-kernel/blob/d47232dfb2b26c0ef18a74e2ef4aa503caa59697/core/org.wso2.carbon.ui/src/main/java/org/wso2/carbon/ui/transports/fileupload/ToolsAnyFileUploadExecutor.java#L36) by `ToolsAnyFileUploadExecutor`:
```java
	@Override
	public boolean execute(HttpServletRequest request,
			HttpServletResponse response) throws CarbonException, IOException {
		PrintWriter out = response.getWriter();
        try {
        	Map fileResourceMap =
                (Map) configurationContext
                        .getProperty(ServerConstants.FILE_RESOURCE_MAP);
        	if (fileResourceMap == null) {
        		fileResourceMap = new TreeBidiMap();
        		configurationContext.setProperty(ServerConstants.FILE_RESOURCE_MAP,
                                             fileResourceMap);
        	}
            List<FileItemData> fileItems = getAllFileItems();
            //String filePaths = "";

            for (FileItemData fileItem : fileItems) {
                String uuid = String.valueOf(
                        System.currentTimeMillis() + Math.random());
                String serviceUploadDir =
                        configurationContext
                                .getProperty(ServerConstants.WORK_DIR) +
                                File.separator +
                                "extra" + File
                                .separator +
                                uuid + File.separator;
                File dir = new File(serviceUploadDir);
                if (!dir.exists()) {
                    dir.mkdirs();
                }
                File uploadedFile = new File(dir, fileItem.getFileItem().getFieldName());
                try (FileOutputStream fileOutStream = new FileOutputStream(uploadedFile)) {
                    fileItem.getDataHandler().writeTo(fileOutStream);
                    fileOutStream.flush();
                }
                response.setContentType("text/plain; charset=utf-8");
                //filePaths = filePaths + uploadedFile.getAbsolutePath() + ",";
                fileResourceMap.put(uuid, uploadedFile.getAbsolutePath());
                out.write(uuid);
            }
            //filePaths = filePaths.substring(0, filePaths.length() - 1);
            //out.write(filePaths);
            out.flush();
        } catch (Exception e) {
            log.error("File upload FAILED", e);
            out.write("<script type=\"text/javascript\">" +
                    "top.wso2.wsf.Util.alertWarning('File upload FAILED. File may be non-existent or invalid.');" +
                    "</script>");
        } finally {
            out.close();
        }
        return true;
	}
```
Here is where the bug lies, `execute()` method is vulnerable to a path traversal vulenerabulity as it trusts the filename given by the user in the POST request. without the path traversal escaping the tmp dir the file is actually saved to:
```
./tmp/work/extra/$uuid/$filename
```
with `uuid` being returned in the response:

![image](https://user-images.githubusercontent.com/67718634/164338439-5cc7871c-9bab-4c7d-ba98-d243e8d8ad39.png)

the file can be found in:

![image](https://user-images.githubusercontent.com/67718634/164338596-8d999333-6d8b-4d6d-a082-934c681033fa.png)

Now we just need to escape the `tmp` directory and add our JSP shell to some location being served by the WSO2.

lets find the tomcat `appBase` directory:

![image](https://user-images.githubusercontent.com/67718634/164561581-c3fd8abd-ae43-4fd3-bc6a-de4728c31f1e.png)

this directory is the location of the applications that are deployed on tomcat, it contains multiple already deployed WAR applications and also thier raw WAR files:
```
./repository/deployment/server/webapps
```
![image](https://user-images.githubusercontent.com/67718634/164625750-4fa2742f-815e-49ba-a94e-6eb857d7a0b2.png)

one of those applications is `authenticationendpoint` (`//host/authenticationendpoint`) which handles the authentication to WSO2 and its location is:
```
./repository/deployment/server/webapps/authenticationendpoint
```
![image](https://user-images.githubusercontent.com/67718634/164626950-fcfa4d13-99e1-41f5-9c9f-8ba6a8fc0a18.png)

**NOTE:** we can also use the vulnerability to create our own fresh directory (context path) in the `appBase` directory and it will be auto deployed, but i will just carry one and use `authenticationendpoint`.
# PoC
* Using Burpsuite:

![image](https://user-images.githubusercontent.com/67718634/164339943-588e6879-e93c-4392-9300-d51c6ccb3fe9.png)

![image](https://user-images.githubusercontent.com/67718634/164340091-70bfd623-526d-45a5-a9ee-89912a4a1cd2.png)

![image](https://user-images.githubusercontent.com/67718634/164340406-8c18a647-5e67-4a21-b426-964b8c0c63f6.png)

* Using exploiy.py:

> Usage: 
> ```
> python3 exploit.py https://host:9443/ ArbitraryShellName.jsp
> ```
![poc](https://user-images.githubusercontent.com/67718634/164464002-e31867e8-68cc-4f66-a77b-00515c486f8e.gif)

