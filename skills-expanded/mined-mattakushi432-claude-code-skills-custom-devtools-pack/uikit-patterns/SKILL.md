---
name: uikit-patterns
description: "When to activate: UIKit, UIViewController, UITableView, UICollectionView, Auto Layout, view lifecycle, UINavigationController"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: swift
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# UIKit Patterns

## ViewController Lifecycle

```swift
final class ArticleViewController: UIViewController {
    // MARK: - Subviews
    private lazy var titleLabel: UILabel = {
        let label = UILabel()
        label.font = .preferredFont(forTextStyle: .headline)
        label.numberOfLines = 0
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }()

    private lazy var bodyTextView: UITextView = {
        let tv = UITextView()
        tv.isEditable = false
        tv.font = .preferredFont(forTextStyle: .body)
        tv.translatesAutoresizingMaskIntoConstraints = false
        return tv
    }()

    // MARK: - Dependencies
    private let article: Article

    init(article: Article) {
        self.article = article
        super.init(nibName: nil, bundle: nil)
    }

    @available(*, unavailable)
    required init?(coder: NSCoder) { fatalError() }

    // MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        setupViews()
        setupConstraints()
        configure(with: article)
    }

    // MARK: - Setup
    private func setupViews() {
        view.backgroundColor = .systemBackground
        view.addSubview(titleLabel)
        view.addSubview(bodyTextView)
    }

    private func setupConstraints() {
        NSLayoutConstraint.activate([
            titleLabel.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 16),
            titleLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
            titleLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16),

            bodyTextView.topAnchor.constraint(equalTo: titleLabel.bottomAnchor, constant: 12),
            bodyTextView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            bodyTextView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            bodyTextView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
        ])
    }

    private func configure(with article: Article) {
        title = article.title
        titleLabel.text = article.title
        bodyTextView.text = article.body
    }
}
```

## UITableView with Diffable Data Source

```swift
final class ItemListViewController: UIViewController {
    enum Section { case main }

    private var tableView: UITableView!
    private var dataSource: UITableViewDiffableDataSource<Section, Item>!

    override func viewDidLoad() {
        super.viewDidLoad()
        configureTableView()
        configureDataSource()
    }

    private func configureTableView() {
        tableView = UITableView(frame: view.bounds, style: .insetGrouped)
        tableView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "Cell")
        view.addSubview(tableView)
    }

    private func configureDataSource() {
        dataSource = UITableViewDiffableDataSource(tableView: tableView) { tableView, indexPath, item in
            let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath)
            var content = cell.defaultContentConfiguration()
            content.text = item.title
            cell.contentConfiguration = content
            return cell
        }
    }

    func update(with items: [Item], animated: Bool = true) {
        var snapshot = NSDiffableDataSourceSnapshot<Section, Item>()
        snapshot.appendSections([.main])
        snapshot.appendItems(items, toSection: .main)
        dataSource.apply(snapshot, animatingDifferences: animated)
    }
}
```

## UICollectionView Compositional Layout

```swift
func makeLayout() -> UICollectionViewLayout {
    UICollectionViewCompositionalLayout { sectionIndex, environment in
        let itemSize = NSCollectionLayoutSize(
            widthDimension: .fractionalWidth(0.5),
            heightDimension: .fractionalHeight(1.0)
        )
        let item = NSCollectionLayoutItem(layoutSize: itemSize)
        item.contentInsets = NSDirectionalEdgeInsets(top: 4, leading: 4, bottom: 4, trailing: 4)

        let groupSize = NSCollectionLayoutSize(
            widthDimension: .fractionalWidth(1.0),
            heightDimension: .absolute(160)
        )
        let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])

        let section = NSCollectionLayoutSection(group: group)
        section.contentInsets = NSDirectionalEdgeInsets(top: 8, leading: 8, bottom: 8, trailing: 8)
        return section
    }
}
```

## Navigation Patterns

```swift
// Coordinator pattern — decouples view controllers from navigation
protocol Coordinator: AnyObject {
    var navigationController: UINavigationController { get }
    func start()
}

final class ArticleCoordinator: Coordinator {
    let navigationController: UINavigationController

    init(navigationController: UINavigationController) {
        self.navigationController = navigationController
    }

    func start() {
        let vc = ArticleListViewController()
        vc.delegate = self
        navigationController.pushViewController(vc, animated: false)
    }
}

extension ArticleCoordinator: ArticleListViewControllerDelegate {
    func didSelect(article: Article) {
        let vc = ArticleViewController(article: article)
        navigationController.pushViewController(vc, animated: true)
    }
}
```

## Common Anti-Patterns

- **Massive ViewControllers** — use Coordinator + ViewModel pattern to separate concerns
- **Layout in `viewDidLayoutSubviews`** — set constraints once in `viewDidLoad`
- **Retain cycles in closures** — use `[weak self]` in animation blocks and callbacks
- **Storing index paths** — use diffable data sources with stable identifiers
- **`storyboard` for complex flows** — prefer programmatic UI for testability and merge conflict avoidance
