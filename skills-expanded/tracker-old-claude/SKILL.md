# Tracker Projects Instructions
## Tech Stack
- Target iOS 26
- Core app must be written in UIKit 
- uses CoreData in iCloud for storage sync
- Be written in swift 6
- Uses the latest UICollectionView and UIListView technologies
- use xcodegen to manage project
  - run xcodegen any time it requires updating

## Collection and List Views Must follow Modern Patterns:
### Data & cells
- UICollectionViewDiffableDataSource<Section, Item> + NSDiffableDataSourceSnapshot (no reloadData() or index-path math).
- UICollectionView.CellRegistration<Cell, Item> + dequeueConfiguredReusableCell(using:for:item:) (no string reuse IDs).

### ⠀Layout
- Grids: UICollectionViewCompositionalLayout + section provider + NSCollectionLayoutSection/Group; use container size for adaptive columns.
- Lists: UICollectionViewCompositionalLayout.list(using: listConfig) + UICollectionLayoutListConfiguration (appearance, separators, header mode, swipe action providers).

### ⠀List UI
- UICollectionViewListCell + UIListContentConfiguration (e.g. .subtitleCell(), .header()) and cell.accessories.
- Section headers via SupplementaryRegistration<UICollectionViewListCell> + UIListContentConfiguration.header().

### ⠀Integrations
- Core Data: controller(_:didChangeContentWith snapshot:) → build snapshot from reference, use reconfigureItems(reloaded) for in-place updates.
- Reordering: reorderingHandlers.canReorderItem / didReorder and NSDiffableDataSourceTransaction; persist order and temporarily disconnect FRC during reorder.
- Empty state: UIContentUnavailableConfiguration + updateContentUnavailableConfiguration(using:) / setNeedsUpdateContentUnavailableConfiguration().

### ⠀Also use
- viewIsAppearing(_:), UIColorPickerViewController where appropriate.

### ⠀Avoid
- UICollectionViewDataSource, string reuse IDs, UICollectionViewFlowLayout for custom grids.
