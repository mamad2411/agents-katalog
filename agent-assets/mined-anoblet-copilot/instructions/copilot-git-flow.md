# Git Flow: A Successful Git branching model

![Alt Text](https://thepracticaldev.s3.amazonaws.com/i/bzznruj0grqr5mdwbgwz.png)

Gitflow is a Git workflow design that was first published and made popular by [Vincent Driessen at nvie](https://nvie.com/posts/a-successful-git-branching-model/). The Gitflow defines a strict branching model designed around the project release. This provides a robust framework for managing larger projects.

Gitflow is ideally suited for projects that have a scheduled release cycle. This workflow doesn’t add any new concepts or commands beyond what’s required for the [Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). Instead, it assigns very specific roles to different branches and defines how and when they should interact. In addition to feature branches, it uses individual branches for preparing, maintaining, and recording releases. Of course, you also get to leverage all the benefits of the Feature Branch Workflow: pull requests, isolated experiments, and more efficient collaboration.

## Getting started

---

### Installation

- For **OSX**: `brew install git-flow`
- For **Windows**: `https://git-scm.com/download/win`
- For **Linux/Ubuntu**: `sudo apt-get install git-flow`

---

### Initialization

Instead of a single master branch, this workflow uses two branches to record the history of the project. The **master** branch stores the official release history, and the **develop** branch serves as an integration branch for features. It's also convenient to tag all commits in the master branch with a version number.

1. Open terminal or command prompt and goto your project directory(It must be initialised with git).
2. Run `git flow init`

   It will ask some questions about different branches’s naming structure. Please write answers like below.

- Branch name for production releases: `master`
- Branch name for “next release” development: `development`
- Feature branches?: `feature/`
- Bugfix branches?: `bugfix/`
- Release branches?: `release/`
- Hotfix branches?: `hotfix/`
- Support branches?: `support/`
- Version tag prefix?: `v`
- Hooks and filters directory?: press the enter

> **Note:** above options may changes as per the operating systems.
> In some operation systems you won't find **bugfix** or **support** feature.
> But you can manually handle that features.

---

### Feature branches

Feature branches are used to develop new features for the upcoming or a distant future release. The essence of a feature branch is that it exists as long as the feature is in development, but will eventually be merged back into develop or discarded.

![Alt Text](https://thepracticaldev.s3.amazonaws.com/i/gk3yk0u24k5849fplyy2.png)

#### Creating a feature branch

- Run `git flow feature start <<FEATURE_NAME>>`.
- E.g. `git flow feature start authentication`, which creates branch **feature/authentication**.
- Do changes related to that feature and push it to origin.

#### Finishing a feature branch

- Run `git flow feature finish <<FEATURE_NAME>>`.
- E.g. `git flow feature finish authentication`, which merges **feature/authentication** branch into **development** branch and **delete** itself from **local** and **origin**.

#### Summary actions

- Created off to the latest **development** branch.
- After Finishing **feature** branch, it merges into **development** branch and **deletes** feature branch from **local** and **origin**.

---

### Bugfix branches

bugfix branches are used for bug/defect fixing.

#### Creating a bugfix branch

- Run `git flow bugfix start <<BRANCH_NAME>>`.
- E.g. `git flow bugfix start login-bug`, which creates branch **bugfix/login-bug**.
- Do changes related to bug and push it to origin.

#### Finishing a bugfix branch

- Run `git flow bugfix finish <<BRANCH_NAME>>`.
- E.g. `git flow bugfix finish login-bug`, which merges **bugfix/login-bug** branch into **development** branch and **delete** itself from **local** and **origin**.

#### Summary actions

- Created off to the latest **development** branch.
- After Finishing **bugfix** branch, it merges into **development** branch and **deletes** bugfix branch from **local** and **origin**.

---

### Release branches

Release branches support preparation of a new production release. They allow preparing meta-data for a release (version number, build dates, etc.). By doing all of this work on a release branch, the develop branch is cleared to receive features for the next big release.

![Alt Text](https://thepracticaldev.s3.amazonaws.com/i/pyeszwkiezdk5owzq2tq.png)

#### Creating a release branch

- Run `git flow release start <<VERSION_NUMBER>>`.
- E.g. `git flow release start 0.0.1`, which creates branch **release/0.0.1**.
- Do changes related to releasing and push it to origin.

#### Finishing a release branch

- Run `git flow release finish <<VERSION_NUMBER>>`.
- E.g. `git flow release finish 0.0.1`.
- It will ask for release tag message, write proper tag description.
- E.g.

  ```
  ********************************************************
  V0.0.1
  - Integrated Authentication
  - Implemented Login flow
  ********************************************************
  ```

- It creates tag **v0.0.1**.
- **Release** branch merges into **development** and **master** branches and **deletes** it self from **local** and **origin**.
- Don’t forget to push **development** and **master** to push to **origin**.
- Create a **tag** into **github / gitlab / bitbucket** and provide a **tag message**.
- Create a **release / change_log** into **github / gitlab / bitbucket** and provide a proper **release message**.
- Deploy your changes from master to production.
- It helps to record your release history very well.

#### Summary actions

- Created off to the latest **development** branch.
- After Finishing **release** branch, it merges into **master** and **development** branches and **deletes** release branch from **local** and **origin**.
- Creates **release tags** which helps to record **release history**.

---

### Hotfix branches

Hotfix branches are very much like release branches in that they are also meant to prepare for a new production release, albeit unplanned. They arise from the necessity to act immediately upon an undesired state of a live production version. When a critical bug in a production version must be resolved immediately, a hotfix branch may be branched off from the corresponding tag on the master branch that marks the production version. It uses for maintenance or quick patches after release.

![Alt Text](https://thepracticaldev.s3.amazonaws.com/i/wo935eqxtakkfylqzn7y.png)

#### Creating a hotfix branch

- Run `git flow hotfix start <<VERSION_NUMBER>>`.
- E.g. `git flow hotfix start 0.0.2`, which creates branch **hotfix/0.0.2**.
- Do changes related to hotfix and push it to origin.

#### Finishing a hotfix branch

- Run `git flow hotfix finish <<VERSION_NUMBER>>`.
- E.g. `git flow hotfix finish 0.0.2`.
- It will ask for release tag message, write proper tag description.
- E.g.

  ```
  ********************************************************
  V0.0.2
  - Quick patches
  ********************************************************
  ```

- It creates tag **v0.0.2**.
- **Hotfix** branch merges into **development** and **master** branches and **deletes** it self from **local** and **origin**.
- Don’t forget to push **development** and **master** to push to **origin**.
- Create a **tag** into **github / gitlab / bitbucket** and provide a **tag message**.
- Create a **release / change_log** into **github / gitlab / bitbucket** and provide a proper **release message**.
- Deploy your changes from master to production.
- It helps to record your release history very well.

#### Summary actions

- Created off to the latest **master** branch.
- After Finishing **hotfix** branch, it merges into **master** and **development** branches and **deletes** hotfix branch from **local** and **origin**.
- Creates **release tags** which helps to record **release history**.

---

### Support branches

Next to the main branches master and develop, our development model uses a variety of supporting branches to aid parallel development between team members, ease tracking of features, prepare for production releases and to assist in quickly fixing live production problems. Unlike the main branches, these branches always have a limited life time, since they will be removed eventually.

#### Creating a support branch

- Run `git flow support start <<SUPPORT_BRANCH_NAME>> <<EXISTING/ORIGIN/PARENT_BRANCH_NAME>>`.
- E.g. `git flow support start stage-development development` which creates **support/stage-development** branch from **development**.
- Don't forget to push support branch to origin.

#### Summary actions

- Created off to the provided existing branch.
- The different types of branches we may use are:
  - Feature branches
  - Release branches
  - Hotfix branches

---

At the core, the development model is greatly inspired by existing models out there. The central repo holds two main branches with an infinite lifetime:

- Master
- Development

---

### References:

- https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow
- https://nvie.com/posts/a-successful-git-branching-model/
