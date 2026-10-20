# Active Directory ACL Abuse Analysis Skill

This security skill enables detection of dangerous Access Control List misconfigurations in Active Directory environments. It leverages the ldap3 Python library to connect to Domain Controllers and identify permission abuse vectors.

## Key Capabilities

The tool identifies critical permission vulnerabilities including:
- **GenericAll**: Full control over target objects
- **WriteDACL**: Ability to modify permissions
- **WriteOwner**: Permission to take ownership
- **GenericWrite**: Rights to modify object attributes

## Technical Approach

The analysis follows a systematic process: establishing LDAP connections to domain controllers, querying objects with security descriptors, converting binary descriptors to SDDL format, resolving SIDs to readable principals, and flagging dangerous permission grants to non-administrative users.

## Threat Context

This detection addresses MITRE ATT&CK techniques including T1098 (Account Manipulation), T1484.001 (Domain Policy Modification), and T1222.001 (File and Directory Permissions Modification). These misconfigurations form the basis of privilege escalation attack paths discovered by security tools like BloodHound.

## Operational Use

SOC analysts employ this skill during incident investigations, threat hunting operations, and security monitoring validation. The tool generates structured JSON reports documenting affected objects, non-privileged trustees with excessive permissions, and remediation guidance.
