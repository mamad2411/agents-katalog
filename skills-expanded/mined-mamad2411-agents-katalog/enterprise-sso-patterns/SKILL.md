---
name: enterprise-sso-patterns
description: Enterprise SSO implementation — SAML, OIDC, JIT provisioning, SCIM
triggers: [SSO, single sign-on, SAML, OIDC, OAuth, enterprise auth, JIT provisioning, SCIM]
---

# SKILL: Enterprise SSO Patterns

## SAML 2.0 Flow

```python
from onelogin.saml2.auth import OneLogin_Saml2_Auth

@app.route('/saml/login')
def saml_login():
    req = prepare_request()
    auth = OneLogin_Saml2_Auth(req, saml_settings)
    return redirect(auth.login())  # Redirect to IdP

@app.route('/saml/acs', methods=['POST'])
def saml_acs():
    """Assertion Consumer Service"""
    req = prepare_request()
    auth = OneLogin_Saml2_Auth(req, saml_settings)
    auth.process_response()
    
    if auth.is_authenticated():
        user_data = {
            'email': auth.get_nameid(),
            'attributes': auth.get_attributes()
        }
        # Create/update user (JIT provisioning)
        user = get_or_create_user(user_data)
        login_user(user)
        return redirect('/dashboard')
```

## OIDC (OpenID Connect)

```python
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)
oauth.register(
    name='okta',
    client_id=OKTA_CLIENT_ID,
    client_secret=OKTA_CLIENT_SECRET,
    server_metadata_url=f'{OKTA_DOMAIN}/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/login/okta')
def oidc_login():
    redirect_uri = url_for('oidc_callback', _external=True)
    return oauth.okta.authorize_redirect(redirect_uri)

@app.route('/callback')
def oidc_callback():
    token = oauth.okta.authorize_access_token()
    user_info = token['userinfo']
    # JIT provision user
```

## JIT (Just-In-Time) Provisioning

```python
def get_or_create_user(saml_data):
    """Create user on first SSO login"""
    email = saml_data['email']
    
    user = db.query(User).filter_by(email=email).first()
    if not user:
        # Create new user
        user = User(
            email=email,
            name=saml_data['attributes']['firstName'][0],
            role=determine_role(saml_data['attributes'])
        )
        db.add(user)
        db.commit()
    
    return user
```

## SCIM (System for Cross-domain Identity Management)

```python
@app.route('/scim/v2/Users', methods=['POST'])
def scim_create_user():
    """SCIM endpoint for user provisioning"""
    data = request.json
    
    user = User(
        email=data['userName'],
        name=data['name']['formatted'],
        active=data.get('active', True)
    )
    db.add(user)
    db.commit()
    
    return jsonify({
        "id": user.id,
        "userName": user.email,
        "active": user.active
    })

@app.route('/scim/v2/Users/<user_id>', methods=['DELETE'])
def scim_delete_user(user_id):
    """SCIM user deprovisioning"""
    user = User.query.get(user_id)
    user.active = False
    db.commit()
```

## Quality Checks
- [ ] SAML or OIDC implemented
- [ ] JIT provisioning configured
- [ ] SCIM endpoints for provisioning/deprovisioning
- [ ] Multi-IdP support (Okta, Azure AD, Google)
- [ ] Role mapping from IdP attributes
- [ ] Session management
- [ ] Logout flow (SLO for SAML)
- [ ] Metadata endpoints exposed
