---
name: uicollectionview-diffable
description: Build UICollectionView screens using UICollectionViewDiffableDataSource, NSDiffableDataSourceSnapshot, and UICollectionViewCompositionalLayout. Use when creating a new collection view controller, adding diffable data source support, or building compositional layouts with sections and items.
---

# UICollectionView with Diffable Data Source

Use this skill when building a `UICollectionView` screen using `UICollectionViewDiffableDataSource`, `NSDiffableDataSourceSnapshot`, and `UICollectionViewCompositionalLayout`.

## Class Structure

Subclass `UICollectionViewController` directly. Override `loadView()` to replace the default collection view with one that uses the custom compositional layout:

```swift
override func loadView() {
    self.collectionView = UICollectionView(frame: .zero, collectionViewLayout: self.layout)
}
```

When subclassing an intermediate base class that already provides a collection view, assign the layout in `viewDidLoad()` instead:

```swift
override func viewDidLoad() {
    super.viewDidLoad()
    self.collectionView.collectionViewLayout = self.layout
}
```

## View Model

The view controller should always be driven by a view model. The view model is the single source of truth for the data displayed in the collection view. The view controller subscribes to view model changes and rebuilds the snapshot from the view model's current state.

### View Model Design

The view model should:

- Expose `@Published` properties (or Combine publishers) that represent the current displayable state
- Own the data fetching, transformation, and business logic
- Expose simple, observable properties that the view controller binds to
- Not reference UIKit types

The view model can expose its state in different ways depending on complexity:

**Single published content property** — when the view controller displays a unified set of data:

```swift
final class SettingsViewModel {
    @Published private(set) var content: Content
    @Published private(set) var error: Error?

    struct Content {
        let user: UserModel?
        let plan: PlanModel?
    }

    func refresh() {
        // fetch data and update content
    }
}
```

**View state enum** — when the view controller has multiple distinct display states (loading, error, content, permissions, etc.):

```swift
@MainActor final class DetailViewModel {
    @Published private(set) var viewState: ViewState = .notDetermined
    @Published private(set) var loadState: LoadState = .idle

    enum ViewState {
        case notDetermined
        case permissionRequired(PermissionContent)
        case contentAvailable(ContentData)
        case offline(OfflineContent)
    }

    enum LoadState {
        case idle
        case loading
        case error(Error)
    }

    func refresh() {
        loadState = .loading
        // fetch data, then update viewState and loadState
    }
}
```

### Initial Snapshot and Subscribing to Changes

When first configuring the view controller, immediately build and apply the snapshot without animation. This ensures the collection view renders its content instantly when first displayed.

Then subscribe to the view model's published properties using `dropFirst()` in the publisher chain. Because the initial value was already consumed when building the first snapshot, `dropFirst()` skips the redundant initial emission. All subsequent updates from these publishers are applied with animation. This avoids an awkward animation on first display while still animating real data changes.

```swift
private var subscribers: Set<AnyCancellable> = .init()

func configure(viewModel: ExampleViewModel) {
    self.subscribers.removeAll()
    self.viewModel = viewModel

    // immediately render the current state without animation
    self.applySnapshot(animated: false)

    // subscribe to future changes; dropFirst skips the initial value
    // that was already consumed above
    viewModel.$content
        .dropFirst()
        .receive(on: DispatchQueue.main)
        .sink { [weak self] _ in
            self?.applySnapshot(animated: true)
        }
        .store(in: &subscribers)
}
```

For view state enums, the same pattern applies — apply the initial state immediately, then subscribe with `dropFirst()`:

```swift
func configure(viewModel: DetailViewModel) {
    self.subscribers.removeAll()
    self.viewModel = viewModel

    // render current state immediately
    self.updateView(with: viewModel.viewState, animated: false)

    // subscribe to future state changes
    viewModel.$viewState
        .dropFirst()
        .receive(on: DispatchQueue.main)
        .sink { [weak self] state in
            self?.updateView(with: state, animated: true)
        }
        .store(in: &subscribers)

    viewModel.$loadState
        .dropFirst()
        .receive(on: DispatchQueue.main)
        .sink { [weak self] loadState in
            self?.updateLoadingState(loadState)
        }
        .store(in: &subscribers)
}

private func updateView(with state: DetailViewModel.ViewState, animated: Bool) {
    switch state {
    case .notDetermined:
        break
    case .contentAvailable(let content):
        self.applyContentSnapshot(for: content, animated: animated)
    case .permissionRequired(let content):
        self.applyPermissionSnapshot(for: content, animated: animated)
    case .offline(let content):
        self.applyOfflineSnapshot(for: content, animated: animated)
    }
}
```

### Key Principles

- The view controller never fetches data or performs business logic directly
- The `createSnapshot()` method reads from the view model to decide which sections and items to include
- Multiple view model properties can each trigger snapshot rebuilds independently
- Always apply the initial snapshot with `animated: false` at configuration time, then use `dropFirst()` on publishers so subsequent updates animate naturally
- Store subscribers in a `Set<AnyCancellable>` property and cancel them when the view model is replaced

## Types

Define all types as nested types inside the class, grouped under `// MARK: - Types`.

### Section

`Section` is an enum representing each distinct content group. Choose the raw type based on needs:

- `Int, CaseIterable` — when sections have a fixed, ordered set of cases
- `String` — when sections need a string-based raw value (e.g. for titles)
- Plain `Hashable` (no raw type) — when sections carry associated values

```swift
private enum Section: Int, CaseIterable {
    case header
    case content
    case footer
}
```

Or with associated values:

```swift
enum Section: Hashable {
    case historical(HistoryModel)
    case forecast(ForecastModel)
}
```

### Item

`Item` is an enum or struct conforming to `Hashable` with one case per distinct cell type. Cases carry associated model values that the cell needs for configuration.

**Enum form** — when each case maps directly to a cell type and the associated values are already `Hashable`:

```swift
private enum Item: Hashable {
    case setting(SettingModel)
    case copyright
}
```

**Struct form** — when items share a common structure or need a nested `Content` enum for variant data:

```swift
struct Item: Hashable {
    enum Content {
        case group(Group)
        case podcast(Podcast)
        case empty
    }

    let content: Content

    func hash(into hasher: inout Hasher) {
        switch content {
        case .group(let group):
            hasher.combine(group.id)
        case .podcast(let podcast):
            hasher.combine(podcast.id)
        case .empty:
            hasher.combine("empty")
        }
    }

    static func == (lhs: Item, rhs: Item) -> Bool {
        lhs.hashValue == rhs.hashValue
    }
}
```

For complex enum cases where items need custom identity or equality, also conform to `Identifiable` and provide explicit `hash(into:)` and `==`:

```swift
private enum Item: Identifiable, Hashable {
    case weather(WeatherModel)
    case forecast(ForecastContent)
    case moreInfo(MoreInfoRow, ForecastContent)

    var id: String {
        switch self {
        case .weather(let model):
            return "weather :: \(model.displayAt)"
        case .forecast(let content):
            return "forecast :: \(content.id)"
        case .moreInfo(let row, _):
            return "moreInfo :: \(row.rawValue)"
        }
    }

    func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }

    static func == (lhs: Item, rhs: Item) -> Bool {
        lhs.id == rhs.id
    }
}
```

### Typealiases

Always define these two typealiases after the type definitions:

```swift
private typealias DataSource = UICollectionViewDiffableDataSource<Section, Item>
private typealias Snapshot = NSDiffableDataSourceSnapshot<Section, Item>
```

Use `fileprivate` instead of `private` when the types or aliases need to be visible to extensions in the same file that are not nested inside the class body.

## Data Source

Define `dataSource` as a `private lazy var`. The initializer closure calls a private method for cell creation. Assign `supplementaryViewProvider` in the same block. Always capture `self` weakly.

```swift
private lazy var dataSource: DataSource = {
    let dataSource = DataSource(collectionView: self.collectionView) { [weak self] collectionView, indexPath, item in
        self?.cell(in: collectionView, at: indexPath, item: item)
    }

    dataSource.supplementaryViewProvider = { [weak self] collectionView, kind, indexPath in
        self?.supplementaryView(in: collectionView, ofKind: kind, at: indexPath)
    }

    return dataSource
}()
```

## Layout

Define `layout` as a `private lazy var` using the section-provider initializer. Look up the `Section` from `self.dataSource.sectionIdentifier(for:)` and dispatch to a layout method.

```swift
private lazy var layout: UICollectionViewCompositionalLayout = {
    UICollectionViewCompositionalLayout { [weak self] sectionIndex, environment in
        guard let self, let section = self.dataSource.sectionIdentifier(for: sectionIndex) else {
            return nil
        }
        return self.sectionLayout(section, environment: environment)
    }
}()
```

### Section Layout Method

Define a private method that switches on the section and returns an `NSCollectionLayoutSection`. Build each section using standard `NSCollectionLayoutItem`, `NSCollectionLayoutGroup`, and `NSCollectionLayoutSection` APIs:

```swift
private func sectionLayout(_ section: Section, environment: NSCollectionLayoutEnvironment) -> NSCollectionLayoutSection? {
    switch section {
    case .content:
        let itemSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(1.0), heightDimension: .estimated(175.0))
        let item = NSCollectionLayoutItem(layoutSize: itemSize)

        let groupSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(1.0), heightDimension: .estimated(175.0))
        let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])

        let section = NSCollectionLayoutSection(group: group)
        section.contentInsets = NSDirectionalEdgeInsets(top: 0, leading: 16, bottom: 16, trailing: 16)

        let headerSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(1.0), heightDimension: .estimated(45.0))
        let header = NSCollectionLayoutBoundarySupplementaryItem(
            layoutSize: headerSize,
            elementKind: UICollectionView.elementKindSectionHeader,
            alignment: .top
        )
        section.boundarySupplementaryItems = [header]

        return section

    case .footer:
        let itemSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(1.0), heightDimension: .estimated(48.0))
        let item = NSCollectionLayoutItem(layoutSize: itemSize)
        let group = NSCollectionLayoutGroup.horizontal(layoutSize: itemSize, subitems: [item])

        let section = NSCollectionLayoutSection(group: group)
        section.contentInsets = NSDirectionalEdgeInsets(top: 16, leading: 16, bottom: 16, trailing: 16)
        return section
    }
}
```

### Section Inset Guidelines

When determining section insets for card-style layouts:

- **Section has a header view:** use `0` for `top`, and a standard margin for `bottom`.
- **Section does not have a header view:** use a standard margin for both `top` and `bottom`.

## Cell and Supplementary View Registration

Register cells and supplementary views in a `setupCollectionView()` method called from `viewDidLoad()`. Use standard UIKit registration APIs:

```swift
private func setupCollectionView() {
    collectionView.backgroundColor = .systemBackground
    collectionView.register(ContentCell.self, forCellWithReuseIdentifier: ContentCell.reuseIdentifier)
    collectionView.register(FooterCell.self, forCellWithReuseIdentifier: FooterCell.reuseIdentifier)
    collectionView.register(
        SectionHeaderView.self,
        forSupplementaryViewOfKind: UICollectionView.elementKindSectionHeader,
        withReuseIdentifier: SectionHeaderView.reuseIdentifier
    )
}
```

If the project provides typed convenience extensions for `register` and `dequeue` (e.g. a `NibReusable` or `Reusable` protocol), prefer those over raw string identifiers.

## Cell and Supplementary View Dequeue

Use standard UIKit dequeue methods, casting to the expected type:

```swift
// cells
let cell = collectionView.dequeueReusableCell(
    withReuseIdentifier: ContentCell.reuseIdentifier,
    for: indexPath
) as! ContentCell

// supplementary views
let header = collectionView.dequeueReusableSupplementaryView(
    ofKind: UICollectionView.elementKindSectionHeader,
    withReuseIdentifier: SectionHeaderView.reuseIdentifier,
    for: indexPath
) as! SectionHeaderView
```

If the project provides typed convenience extensions for dequeue, prefer those over raw casts.

## Cell Provider Method

Define a private method that switches on the `Item` and dequeues/configures the appropriate cell. This method is called by the data source closure.

```swift
private func cell(in collectionView: UICollectionView, at indexPath: IndexPath, item: Item) -> UICollectionViewCell? {
    switch item {
    case .content(let model):
        let cell = collectionView.dequeueReusableCell(
            withReuseIdentifier: ContentCell.reuseIdentifier,
            for: indexPath
        ) as! ContentCell
        cell.configure(with: model)
        return cell

    case .footer:
        return collectionView.dequeueReusableCell(
            withReuseIdentifier: FooterCell.reuseIdentifier,
            for: indexPath
        ) as! FooterCell
    }
}
```

## Supplementary View Provider Method

Define a private method that looks up the `Section` for the index path and configures the supplementary view accordingly:

```swift
private func supplementaryView(in collectionView: UICollectionView, ofKind kind: String, at indexPath: IndexPath) -> UICollectionReusableView? {
    guard let section = dataSource.sectionIdentifier(for: indexPath.section) else { return nil }

    let header = collectionView.dequeueReusableSupplementaryView(
        ofKind: kind,
        withReuseIdentifier: SectionHeaderView.reuseIdentifier,
        for: indexPath
    ) as! SectionHeaderView
    header.configure(for: section)
    return header
}
```

## Snapshots

### Building a Snapshot

Define a private `createSnapshot() -> Snapshot` method that builds the full snapshot from scratch. Conditionally append sections and items based on the available data:

```swift
private func createSnapshot() -> Snapshot {
    var snapshot = Snapshot()

    if viewModel.hasContent {
        snapshot.appendSections([.content])
        snapshot.appendItems(viewModel.items.map { .content($0) }, toSection: .content)
    }

    snapshot.appendSections([.footer])
    snapshot.appendItems([.footer], toSection: .footer)

    return snapshot
}
```

### Applying a Snapshot

Define a private `applySnapshot(animated: Bool)` method. Always pass the `animated` parameter through to `animatingDifferences:`:

```swift
private func applySnapshot(animated: Bool) {
    let snapshot = createSnapshot()
    dataSource.apply(snapshot, animatingDifferences: animated)
}
```

### Reloading Visible Items

To reload all currently displayed items without rebuilding the snapshot (e.g. after a settings change):

```swift
private func reloadAllItems(animated: Bool) {
    var snapshot = dataSource.snapshot()
    guard snapshot.numberOfItems > 0 else { return }
    snapshot.reconfigureItems(snapshot.itemIdentifiers)
    dataSource.apply(snapshot, animatingDifferences: animated)
}
```

### Reloading Visible Sections

To reload only the sections currently visible on screen:

```swift
private func reloadVisibleSections(animated: Bool) {
    var snapshot = dataSource.snapshot()
    let headerIndexPaths = collectionView.indexPathsForVisibleSupplementaryElements(
        ofKind: UICollectionView.elementKindSectionHeader
    )
    let sections = headerIndexPaths.compactMap {
        dataSource.sectionIdentifier(for: $0.section)
    }
    snapshot.reloadSections(sections)
    dataSource.apply(snapshot, animatingDifferences: animated)
}
```

## MARK Organization

Organize the file using these MARK sections in order. Use `private extension` for implementation details and `internal extension` for methods called by parent coordinators or delegates:

```
// MARK: - Types
// MARK: - Properties
// MARK: - UICollectionView Overrides   (or "UIViewController")
// MARK: - Setup                        (collection view setup, bindings)
// MARK: - Configuration                (view model assignment)
// MARK: - Snapshots
// MARK: - Layout
// MARK: - Collection Views             (cell and supplementary creation)
// MARK: - <DelegateName>              (one per delegate conformance)
```

## Complete Skeleton

```swift
import Combine
import UIKit

final class ExampleCollectionViewController: UICollectionViewController {

    // MARK: - Types

    private enum Section: Int, CaseIterable {
        case content
        case footer
    }

    private enum Item: Hashable {
        case content(ContentModel)
        case footer
    }

    private typealias DataSource = UICollectionViewDiffableDataSource<Section, Item>
    private typealias Snapshot = NSDiffableDataSourceSnapshot<Section, Item>

    // MARK: - Properties

    private var viewModel: ExampleViewModel!
    private var subscribers: Set<AnyCancellable> = .init()

    private lazy var dataSource: DataSource = {
        let dataSource = DataSource(collectionView: self.collectionView) { [weak self] collectionView, indexPath, item in
            self?.cell(in: collectionView, at: indexPath, item: item)
        }
        dataSource.supplementaryViewProvider = { [weak self] collectionView, kind, indexPath in
            self?.supplementaryView(in: collectionView, ofKind: kind, at: indexPath)
        }
        return dataSource
    }()

    private lazy var layout: UICollectionViewCompositionalLayout = {
        UICollectionViewCompositionalLayout { [weak self] sectionIndex, environment in
            guard let self, let section = self.dataSource.sectionIdentifier(for: sectionIndex) else {
                return nil
            }
            return self.sectionLayout(section, environment: environment)
        }
    }()
}

// MARK: - UICollectionView Overrides

extension ExampleCollectionViewController {

    override func loadView() {
        self.collectionView = UICollectionView(frame: .zero, collectionViewLayout: self.layout)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        setupCollectionView()
    }
}

// MARK: - Setup

private extension ExampleCollectionViewController {

    func setupCollectionView() {
        collectionView.backgroundColor = .systemBackground
        collectionView.register(ContentCell.self, forCellWithReuseIdentifier: ContentCell.reuseIdentifier)
        collectionView.register(FooterCell.self, forCellWithReuseIdentifier: FooterCell.reuseIdentifier)
        collectionView.register(
            SectionHeaderView.self,
            forSupplementaryViewOfKind: UICollectionView.elementKindSectionHeader,
            withReuseIdentifier: SectionHeaderView.reuseIdentifier
        )
    }
}

// MARK: - Configuration

extension ExampleCollectionViewController {

    func configure(viewModel: ExampleViewModel) {
        self.subscribers.removeAll()
        self.viewModel = viewModel

        self.applySnapshot(animated: false)

        viewModel.$content
            .dropFirst()
            .receive(on: DispatchQueue.main)
            .sink { [weak self] _ in
                self?.applySnapshot(animated: true)
            }
            .store(in: &subscribers)
    }
}

// MARK: - Snapshots

private extension ExampleCollectionViewController {

    func createSnapshot() -> Snapshot {
        var snapshot = Snapshot()

        snapshot.appendSections([.content])
        snapshot.appendItems(viewModel.items.map { .content($0) }, toSection: .content)

        snapshot.appendSections([.footer])
        snapshot.appendItems([.footer], toSection: .footer)

        return snapshot
    }

    func applySnapshot(animated: Bool) {
        let snapshot = createSnapshot()
        dataSource.apply(snapshot, animatingDifferences: animated)
    }
}

// MARK: - Layout

private extension ExampleCollectionViewController {

    func sectionLayout(_ section: Section, environment: NSCollectionLayoutEnvironment) -> NSCollectionLayoutSection? {
        switch section {
        case .content:
            let itemSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(1.0), heightDimension: .estimated(175.0))
            let item = NSCollectionLayoutItem(layoutSize: itemSize)
            let group = NSCollectionLayoutGroup.horizontal(layoutSize: itemSize, subitems: [item])

            let sectionLayout = NSCollectionLayoutSection(group: group)
            sectionLayout.contentInsets = NSDirectionalEdgeInsets(top: 0, leading: 16, bottom: 16, trailing: 16)

            let headerSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(1.0), heightDimension: .estimated(45.0))
            let header = NSCollectionLayoutBoundarySupplementaryItem(
                layoutSize: headerSize,
                elementKind: UICollectionView.elementKindSectionHeader,
                alignment: .top
            )
            sectionLayout.boundarySupplementaryItems = [header]
            return sectionLayout

        case .footer:
            let itemSize = NSCollectionLayoutSize(widthDimension: .fractionalWidth(1.0), heightDimension: .estimated(48.0))
            let item = NSCollectionLayoutItem(layoutSize: itemSize)
            let group = NSCollectionLayoutGroup.horizontal(layoutSize: itemSize, subitems: [item])

            let sectionLayout = NSCollectionLayoutSection(group: group)
            sectionLayout.contentInsets = NSDirectionalEdgeInsets(top: 16, leading: 16, bottom: 16, trailing: 16)
            return sectionLayout
        }
    }
}

// MARK: - Collection Views

private extension ExampleCollectionViewController {

    func cell(in collectionView: UICollectionView, at indexPath: IndexPath, item: Item) -> UICollectionViewCell? {
        switch item {
        case .content(let model):
            let cell = collectionView.dequeueReusableCell(
                withReuseIdentifier: ContentCell.reuseIdentifier,
                for: indexPath
            ) as! ContentCell
            cell.configure(with: model)
            return cell

        case .footer:
            return collectionView.dequeueReusableCell(
                withReuseIdentifier: FooterCell.reuseIdentifier,
                for: indexPath
            ) as! FooterCell
        }
    }

    func supplementaryView(in collectionView: UICollectionView, ofKind kind: String, at indexPath: IndexPath) -> UICollectionReusableView? {
        guard let section = dataSource.sectionIdentifier(for: indexPath.section) else { return nil }

        let header = collectionView.dequeueReusableSupplementaryView(
            ofKind: UICollectionView.elementKindSectionHeader,
            withReuseIdentifier: SectionHeaderView.reuseIdentifier,
            for: indexPath
        ) as! SectionHeaderView
        header.configure(for: section)
        return header
    }
}

// MARK: - UICollectionViewDelegate

extension ExampleCollectionViewController {

    override func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        collectionView.deselectItem(at: indexPath, animated: true)
        guard let item = dataSource.itemIdentifier(for: indexPath) else { return }

        switch item {
        case .content:
            break // handle selection
        case .footer:
            break
        }
    }
}
```
