Now I have everything. Let me write the seed prompt.

---

## Seed Fix Prompt

```
Replace the entire contents of `prisma/seed.ts` with the following.
This seed adds real Unsplash image URLs, creates FileManager records for every
category and product image, and links them properly — matching the exact pattern
used by S3Service (fileType, fileFormat, fileUse, filePath, fileUrl, fileCdnUrl)
and the Category/Product models (imageUrl + fileManagerId).

───────────────────────────────────────────────
prisma/seed.ts
───────────────────────────────────────────────

import { PrismaClient } from '@prisma/client';
import { PrismaPg } from '@prisma/adapter-pg';
import bcrypt from 'bcrypt';

const adapter = new PrismaPg({
  connectionString: process.env.DATABASE_URL!,
});

const prisma = new PrismaClient({ adapter });

// ── helpers ──────────────────────────────────────────────────────────────────

/**
 * Creates a FileManager record that mirrors what S3Service.uploadFile() produces.
 * We use a stable fake S3 key so re-seeding with upsert stays idempotent.
 * The fileCdnUrl points to a real public Unsplash image so the frontend renders it.
 */
async function createFileManager(opts: {
  slug: string;       // unique stable key segment  e.g. "cat-electronics"
  fileUse: string;    // 'category-image' | 'product-image'
  cdnUrl: string;     // real public image URL
}) {
  const ext = 'jpg';
  const fileName = `${opts.slug}.${ext}`;
  const filePath = `raco/${opts.fileUse}/${fileName}`;

  return prisma.fileManager.upsert({
    where: { id: undefined as any },   // no unique slug field — use findFirst guard below
    update: {},
    create: {
      fileName,
      fileType: 'image',
      fileFormat: ext,
      filePath,
      fileUse: opts.fileUse,
      fileBucket: 'seed',
      fileUrl: opts.cdnUrl,
      fileCdnUrl: opts.cdnUrl,
    },
  });
}

/**
 * Idempotent FileManager upsert by filePath (the S3 key is unique per file).
 */
async function getOrCreateFileManager(opts: {
  slug: string;
  fileUse: string;
  cdnUrl: string;
}) {
  const ext = 'jpg';
  const fileName = `${opts.slug}.${ext}`;
  const filePath = `raco/${opts.fileUse}/${fileName}`;

  const existing = await prisma.fileManager.findFirst({ where: { filePath } });
  if (existing) return existing;

  return prisma.fileManager.create({
    data: {
      fileName,
      fileType: 'image',
      fileFormat: ext,
      filePath,
      fileUse: opts.fileUse,
      fileBucket: 'seed',
      fileUrl: opts.cdnUrl,
      fileCdnUrl: opts.cdnUrl,
    },
  });
}

// ── main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log('[SEED] Starting database seed...');

  // ── Admin user ──────────────────────────────────────────────────────────────
  const hashedPassword = await bcrypt.hash('Admin@1234', 12);

  const admin = await prisma.user.upsert({
    where: { email: 'admin@raco.com' },
    update: {},
    create: {
      email: 'admin@raco.com',
      password: hashedPassword,
      name: 'System Administrator',
      role: 'ADMIN',
    },
  });
  console.log('[SEED] Admin user:', admin.email);

  // ── Categories with images ──────────────────────────────────────────────────
  //
  // Tree:
  //   Electronics
  //     ├── Smartphones
  //     ├── Laptops
  //     └── Accessories
  //   Fashion
  //     ├── Men's Clothing
  //     └── Women's Clothing
  //   Home & Living
  //     ├── Furniture
  //     └── Kitchen
  //   Sports & Outdoors
  //     └── Fitness Equipment
  //   Books & Stationery

  const categoryDefs: Array<{
    key: string;
    name: string;
    description: string;
    parentKey: string | null;
    imageUrl: string;
  }> = [
    // ── Root categories
    {
      key: 'electronics',
      name: 'Electronics',
      description: 'Electronic devices, gadgets and accessories',
      parentKey: null,
      imageUrl:
        'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=600&q=80',
    },
    {
      key: 'fashion',
      name: 'Fashion',
      description: 'Clothing, shoes and fashion accessories',
      parentKey: null,
      imageUrl:
        'https://images.unsplash.com/photo-1445205170230-053b83016050?w=600&q=80',
    },
    {
      key: 'home-living',
      name: 'Home & Living',
      description: 'Furniture, decor and everyday home essentials',
      parentKey: null,
      imageUrl:
        'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=600&q=80',
    },
    {
      key: 'sports',
      name: 'Sports & Outdoors',
      description: 'Sports equipment and outdoor gear',
      parentKey: null,
      imageUrl:
        'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=600&q=80',
    },
    {
      key: 'books',
      name: 'Books & Stationery',
      description: 'Books, notebooks and office supplies',
      parentKey: null,
      imageUrl:
        'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=600&q=80',
    },

    // ── Electronics children
    {
      key: 'smartphones',
      name: 'Smartphones',
      description: 'Mobile phones and smartphone accessories',
      parentKey: 'electronics',
      imageUrl:
        'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=600&q=80',
    },
    {
      key: 'laptops',
      name: 'Laptops',
      description: 'Laptop computers for work and gaming',
      parentKey: 'electronics',
      imageUrl:
        'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=600&q=80',
    },
    {
      key: 'accessories',
      name: 'Accessories',
      description: 'Cables, chargers, cases and peripherals',
      parentKey: 'electronics',
      imageUrl:
        'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=600&q=80',
    },

    // ── Fashion children
    {
      key: 'mens-clothing',
      name: "Men's Clothing",
      description: 'T-shirts, pants, shirts and more for men',
      parentKey: 'fashion',
      imageUrl:
        'https://images.unsplash.com/photo-1516257984-b1b4d707412e?w=600&q=80',
    },
    {
      key: 'womens-clothing',
      name: "Women's Clothing",
      description: 'Dresses, tops, skirts and more for women',
      parentKey: 'fashion',
      imageUrl:
        'https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=600&q=80',
    },

    // ── Home & Living children
    {
      key: 'furniture',
      name: 'Furniture',
      description: 'Sofas, chairs, tables and storage',
      parentKey: 'home-living',
      imageUrl:
        'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=600&q=80',
    },
    {
      key: 'kitchen',
      name: 'Kitchen',
      description: 'Cookware, appliances and kitchen essentials',
      parentKey: 'home-living',
      imageUrl:
        'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=600&q=80',
    },

    // ── Sports children
    {
      key: 'fitness',
      name: 'Fitness Equipment',
      description: 'Gym equipment, weights and workout gear',
      parentKey: 'sports',
      imageUrl:
        'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80',
    },
  ];

  // Two-pass insert: roots first, then children (parentKey must already exist)
  const categoryMap = new Map<string, { id: string }>();

  const roots = categoryDefs.filter((c) => !c.parentKey);
  const children = categoryDefs.filter((c) => c.parentKey);

  for (const def of [...roots, ...children]) {
    const fm = await getOrCreateFileManager({
      slug: `cat-${def.key}`,
      fileUse: 'category-image',
      cdnUrl: def.imageUrl,
    });

    const parentId = def.parentKey
      ? categoryMap.get(def.parentKey)?.id ?? null
      : null;

    let cat = await prisma.category.findFirst({ where: { name: def.name } });

    if (!cat) {
      cat = await prisma.category.create({
        data: {
          name: def.name,
          description: def.description,
          parentId,
          imageUrl: fm.fileCdnUrl,
          fileManagerId: fm.id,
        },
      });
    } else {
      // Update image if it was missing
      cat = await prisma.category.update({
        where: { id: cat.id },
        data: {
          imageUrl: fm.fileCdnUrl,
          fileManagerId: fm.id,
        },
      });
    }

    categoryMap.set(def.key, { id: cat.id });
    console.log(`[SEED] Category: ${cat.name} (${cat.id})`);
  }

  // ── Products with images ────────────────────────────────────────────────────
  // Price in Poisha (1 BDT = 100 Poisha)

  const productDefs: Array<{
    sku: string;
    name: string;
    description: string;
    price: number;   // in Poisha
    stock: number;
    categoryKey: string;
    imageUrl: string;
  }> = [
    // ── Smartphones
    {
      sku: 'PHONE-001',
      name: 'iPhone 15 Pro Max',
      description:
        'Apple iPhone 15 Pro Max with A17 Pro chip, 48MP camera system, titanium frame, and up to 29 hours of video playback. Available in 256GB.',
      price: 18500000,   // ৳185,000
      stock: 30,
      categoryKey: 'smartphones',
      imageUrl:
        'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=600&q=80',
    },
    {
      sku: 'PHONE-002',
      name: 'Samsung Galaxy S24 Ultra',
      description:
        'Samsung Galaxy S24 Ultra with Snapdragon 8 Gen 3, built-in S Pen, 200MP camera, and Galaxy AI features. 512GB storage.',
      price: 16500000,   // ৳165,000
      stock: 25,
      categoryKey: 'smartphones',
      imageUrl:
        'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=600&q=80',
    },
    {
      sku: 'PHONE-003',
      name: 'Google Pixel 8 Pro',
      description:
        'Google Pixel 8 Pro with Tensor G3 chip, AI-powered camera, 7 years of updates, and Magic Eraser. 128GB storage.',
      price: 12000000,   // ৳120,000
      stock: 20,
      categoryKey: 'smartphones',
      imageUrl:
        'https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=600&q=80',
    },
    {
      sku: 'PHONE-004',
      name: 'OnePlus 12',
      description:
        'OnePlus 12 with Snapdragon 8 Gen 3, Hasselblad camera tuning, 100W SUPERVOOC charging, and 5400mAh battery.',
      price: 9500000,    // ৳95,000
      stock: 35,
      categoryKey: 'smartphones',
      imageUrl:
        'https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=600&q=80',
    },

    // ── Laptops
    {
      sku: 'LAPTOP-001',
      name: 'MacBook Pro 16" M3 Max',
      description:
        'Apple MacBook Pro 16-inch with M3 Max chip, 36GB unified memory, 1TB SSD, Liquid Retina XDR display, and up to 22 hours battery.',
      price: 35000000,   // ৳350,000
      stock: 15,
      categoryKey: 'laptops',
      imageUrl:
        'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&q=80',
    },
    {
      sku: 'LAPTOP-002',
      name: 'Dell XPS 15 OLED',
      description:
        'Dell XPS 15 with Intel Core i9, RTX 4070, 32GB RAM, 4K OLED display, and 1TB NVMe SSD. Perfect for creative professionals.',
      price: 28500000,   // ৳285,000
      stock: 12,
      categoryKey: 'laptops',
      imageUrl:
        'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=600&q=80',
    },
    {
      sku: 'LAPTOP-003',
      name: 'ASUS ROG Zephyrus G14',
      description:
        'ASUS ROG Zephyrus G14 gaming laptop with AMD Ryzen 9, RTX 4060, 16GB RAM, 1TB SSD, and 165Hz QHD display.',
      price: 22000000,   // ৳220,000
      stock: 18,
      categoryKey: 'laptops',
      imageUrl:
        'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=600&q=80',
    },

    // ── Accessories
    {
      sku: 'ACC-001',
      name: 'AirPods Pro 2nd Gen',
      description:
        'Apple AirPods Pro with Active Noise Cancellation, Transparency mode, Adaptive Audio, and USB-C charging case. Up to 30 hours total.',
      price: 3200000,    // ৳32,000
      stock: 80,
      categoryKey: 'accessories',
      imageUrl:
        'https://images.unsplash.com/photo-1606741965509-717f90af41f1?w=600&q=80',
    },
    {
      sku: 'ACC-002',
      name: 'Sony WH-1000XM5',
      description:
        'Sony WH-1000XM5 wireless headphones with industry-leading noise cancellation, 30-hour battery, and crystal-clear hands-free calling.',
      price: 4500000,    // ৳45,000
      stock: 40,
      categoryKey: 'accessories',
      imageUrl:
        'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600&q=80',
    },
    {
      sku: 'ACC-003',
      name: 'Anker 100W GaN Charger',
      description:
        'Anker 735 GaN Prime 100W 3-port charger. Powers a MacBook Pro and iPhone simultaneously. Compact and travel-friendly.',
      price: 350000,     // ৳3,500
      stock: 150,
      categoryKey: 'accessories',
      imageUrl:
        'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=600&q=80',
    },
    {
      sku: 'ACC-004',
      name: 'Logitech MX Master 3S',
      description:
        'Logitech MX Master 3S wireless mouse with MagSpeed scroll, 8K DPI, silent clicks, and USB-C charging. Works on any surface.',
      price: 1350000,    // ৳13,500
      stock: 60,
      categoryKey: 'accessories',
      imageUrl:
        'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&q=80',
    },

    // ── Men's Clothing
    {
      sku: 'MEN-001',
      name: 'Classic Oxford Shirt',
      description:
        'Premium 100% cotton Oxford shirt with button-down collar. Slim fit, wrinkle-resistant, and perfect for both casual and formal occasions.',
      price: 250000,     // ৳2,500
      stock: 100,
      categoryKey: 'mens-clothing',
      imageUrl:
        'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600&q=80',
    },
    {
      sku: 'MEN-002',
      name: 'Slim Fit Chino Pants',
      description:
        'Versatile slim-fit chino pants made from stretch cotton blend. Available in navy, khaki and olive. Comfortable for all-day wear.',
      price: 350000,     // ৳3,500
      stock: 75,
      categoryKey: 'mens-clothing',
      imageUrl:
        'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=600&q=80',
    },

    // ── Women's Clothing
    {
      sku: 'WOMEN-001',
      name: 'Floral Wrap Dress',
      description:
        'Elegant floral wrap dress in lightweight chiffon fabric. V-neck design with adjustable tie waist. Perfect for summer occasions.',
      price: 450000,     // ৳4,500
      stock: 60,
      categoryKey: 'womens-clothing',
      imageUrl:
        'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600&q=80',
    },
    {
      sku: 'WOMEN-002',
      name: 'Linen Blazer',
      description:
        'Sophisticated single-button linen blazer with a relaxed fit. Breathable and stylish for work or smart-casual outings.',
      price: 650000,     // ৳6,500
      stock: 45,
      categoryKey: 'womens-clothing',
      imageUrl:
        'https://images.unsplash.com/photo-1594938298603-c8148c4b4705?w=600&q=80',
    },

    // ── Furniture
    {
      sku: 'FURN-001',
      name: 'Ergonomic Office Chair',
      description:
        'High-back ergonomic mesh office chair with lumbar support, adjustable armrests, seat height and headrest. Supports up to 150kg.',
      price: 2800000,    // ৳28,000
      stock: 20,
      categoryKey: 'furniture',
      imageUrl:
        'https://images.unsplash.com/photo-1592078615290-033ee584e267?w=600&q=80',
    },
    {
      sku: 'FURN-002',
      name: 'Solid Wood Study Desk',
      description:
        'Minimalist solid sheesham wood study desk with 2 drawers and a cable management hole. Dimensions: 120cm × 60cm × 75cm.',
      price: 3500000,    // ৳35,000
      stock: 15,
      categoryKey: 'furniture',
      imageUrl:
        'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=600&q=80',
    },

    // ── Kitchen
    {
      sku: 'KITCH-001',
      name: 'Philips Air Fryer 4.1L',
      description:
        'Philips Essential Air Fryer with Rapid Air technology. 4.1L capacity, 2000W, dishwasher-safe basket, and 7 preset cooking modes.',
      price: 850000,     // ৳8,500
      stock: 35,
      categoryKey: 'kitchen',
      imageUrl:
        'https://images.unsplash.com/photo-1648383422565-9f00ed49e5c3?w=600&q=80',
    },
    {
      sku: 'KITCH-002',
      name: 'Stainless Steel Cookware Set',
      description:
        '12-piece stainless steel cookware set with tri-ply construction. Includes saucepans, frying pans and stock pot. Induction-compatible.',
      price: 1200000,    // ৳12,000
      stock: 25,
      categoryKey: 'kitchen',
      imageUrl:
        'https://images.unsplash.com/photo-1585515320310-259814833e62?w=600&q=80',
    },

    // ── Fitness
    {
      sku: 'FIT-001',
      name: 'Adjustable Dumbbell Set 5–52.5 lbs',
      description:
        'Bowflex SelectTech adjustable dumbbells that replace 15 sets of weights. Quick dial adjustment from 2.5kg to 24kg. Space-saving design.',
      price: 2500000,    // ৳25,000
      stock: 20,
      categoryKey: 'fitness',
      imageUrl:
        'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&q=80',
    },
    {
      sku: 'FIT-002',
      name: 'Yoga Mat Premium 6mm',
      description:
        'Non-slip eco-friendly TPE yoga mat 6mm thick. Extra wide 183cm × 68cm. Includes carrying strap. Suitable for yoga, pilates and stretching.',
      price: 180000,     // ৳1,800
      stock: 100,
      categoryKey: 'fitness',
      imageUrl:
        'https://images.unsplash.com/photo-1601925228843-f1a93bde2dc5?w=600&q=80',
    },

    // ── Books
    {
      sku: 'BOOK-001',
      name: 'Clean Code by Robert C. Martin',
      description:
        'A handbook of agile software craftsmanship. Essential reading for every developer who wants to write better, maintainable code.',
      price: 120000,     // ৳1,200
      stock: 50,
      categoryKey: 'books',
      imageUrl:
        'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&q=80',
    },
    {
      sku: 'BOOK-002',
      name: 'The Pragmatic Programmer',
      description:
        'From journeyman to master — the classic book that changed how a generation of developers thinks about software. 20th anniversary edition.',
      price: 130000,     // ৳1,300
      stock: 40,
      categoryKey: 'books',
      imageUrl:
        'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=600&q=80',
    },
    {
      sku: 'BOOK-003',
      name: 'Hardcover Dotted Notebook A5',
      description:
        'Premium dotted journal with 192 pages, ivory paper 120gsm, ribbon bookmark, and lay-flat binding. Ideal for bullet journaling.',
      price: 85000,      // ৳850
      stock: 120,
      categoryKey: 'books',
      imageUrl:
        'https://images.unsplash.com/photo-1517971129774-8a2b38fa128e?w=600&q=80',
    },
  ];

  for (const def of productDefs) {
    const categoryId = categoryMap.get(def.categoryKey)?.id;
    if (!categoryId) {
      console.warn(`[SEED] Category not found for key: ${def.categoryKey} — skipping ${def.sku}`);
      continue;
    }

    const fm = await getOrCreateFileManager({
      slug: `prod-${def.sku.toLowerCase()}`,
      fileUse: 'product-image',
      cdnUrl: def.imageUrl,
    });

    await prisma.product.upsert({
      where: { sku: def.sku },
      update: {
        imageUrl: fm.fileCdnUrl,
        fileManagerId: fm.id,
      },
      create: {
        sku: def.sku,
        name: def.name,
        description: def.description,
        price: def.price,
        stock: def.stock,
        categoryId,
        imageUrl: fm.fileCdnUrl,
        fileManagerId: fm.id,
      },
    });

    console.log(`[SEED] Product: ${def.name} (${def.sku})`);
  }

  console.log('\n[SEED] ✅ Database seeded successfully!');
  console.log(`[SEED]    Categories : ${categoryDefs.length}`);
  console.log(`[SEED]    Products   : ${productDefs.length}`);
  console.log('[SEED]    Admin      : admin@raco.com / Admin@1234');
}

main()
  .catch((e) => {
    console.error('[ERROR] Seed failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

**Then run:**

```bash
pnpm run prisma:seed
```
