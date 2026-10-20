# Persistence Rules — Java Examples

**Framework basis:** Java 17+, Spring Boot 3.x (Spring Framework 6, `jakarta.*`),
Spring Data JPA + Hibernate, over an existing SQLite database shared with the
legacy Python backend. The rules themselves are stack-agnostic — these examples
show one concrete stack.
**Translation hints:** Micronaut Data / Quarkus Panache → same repository shape,
different base types; JOOQ/MyBatis → mappers instead of derived queries, same
scoping/bounding rules; plain JDBC → the raw-SQL guidance in the Python file.
**Version-sensitive:** Spring Boot 3.x uses `jakarta.persistence.*` — Boot 2.x
uses `javax.persistence.*`; derived-query parsing and `ddl-auto` behave the same,
only the imports differ. SQLite needs the community Hibernate dialect
(`org.hibernate.community.dialect.SQLiteDialect`).

## Rule 1 — Map to the real schema, exactly
Violation:
```java
@Entity
@Table(name = "students")
public class Student {
    private String firstName;                 // no @Column: naming strategy
                                              // guesses a column name that may
                                              // NOT be `first_name`
    @Column(name = "registered_at")
    private Instant registeredAt;             // DB stores TEXT, not a timestamp
}
```
Correct:
```java
@Entity
@Table(name = "students")
public class Student {
    @Column(name = "first_name", nullable = false)   // explicit, matches the DB
    private String firstName;

    @Column(name = "registered_at", nullable = false)
    private String registeredAt = "";         // TEXT column → String, as stored
}
```

## Rule 2 — Repositories only fetch and persist
Violation:
```java
public interface StudentRepository extends JpaRepository<Student, Long> {
    default Student register(Student s) {     // business logic in the repo
        s.setRegisteredAt(Instant.now().toString());   // rule/clock decision
        if (findByEmail(s.getEmail()).isPresent())
            throw new IllegalStateException("duplicate");
        return save(s);
    }
}
```
Correct:
```java
public interface StudentRepository extends JpaRepository<Student, Long> {
    Optional<Student> findByEmail(String email);      // just a query
}
// registration timing + duplicate rule live in StudentService (service-warden)
```

## Rule 3 — Persistence models stay in the persistence layer
Violation:
```java
@GetMapping("/students")
public List<Student> all() { return studentRepository.findAll(); } // entity on the wire
```
Correct:
```java
// controller/service maps the entity to a DTO at the boundary:
return studentRepository.findAll(Sort.by("id"))
        .stream().map(StudentDto::from).toList();     // StudentDto is the wire shape
```

## Rule 4 — Transaction boundary is the caller's
Violation:
```java
@Repository
class DocumentDao {
    @Transactional                            // repo owns the transaction
    public void saveBoth(Document a, Document b) {
        em.persist(a); em.flush();            // commits mid-operation
        em.persist(b);
    }
}
```
Correct:
```java
// repository just persists; the service method is the unit of work:
@Transactional                                // on the service entry point
public void recordUpload(...) {
    documentRepository.save(first);
    documentRepository.save(second);          // both commit or both roll back
}
```

## Rule 5 — Scope every query to its owner
Violation:
```java
Optional<Document> doc = documentRepository.findById(docId);   // any student's doc
```
Correct:
```java
// SELECT * FROM documents WHERE id = ? AND student_id = ?
Optional<Document> findByIdAndStudentId(Long id, Long studentId);
// a document can't be read or deleted under the wrong student
```

## Rule 6 — Bound every read; avoid N+1
Violation:
```java
List<Student> all = repo.findAll();           // whole table into memory...
long n = all.stream().filter(s -> s.getProgram().equals(p)).count();  // ...to count
for (Student s : all) documentRepository.findByStudentIdOrderByIdDesc(s.getId()); // N+1
```
Correct:
```java
long n = repo.countByProgram(p);                         // count in the DB
Page<Student> page = repo.findAll(PageRequest.of(0, 50)); // bounded read
// need docs per student? one query with a join fetch / @EntityGraph, not a loop
```

## Rule 7 — Prefer derived queries; keep raw SQL parameterized
Violation:
```java
@Query(value = "SELECT * FROM students WHERE email = '" + email + "'",  // injection
       nativeQuery = true)
List<Student> byEmail(String email);
```
Correct:
```java
Optional<Student> findByEmail(String email);             // derived, no SQL at all
// if raw SQL is truly needed, bind parameters — never concatenate:
@Query(value = "SELECT * FROM students WHERE email = :email", nativeQuery = true)
Optional<Student> byEmail(@Param("email") String email);
```

## Rule 8 — Model relationships deliberately; match existing semantics
Violation:
```java
@Entity @Table(name = "documents")
public class Document {
    @ManyToOne(cascade = CascadeType.ALL)     // silently adds cascade delete +
    private Student student;                   // lazy loading the app never had
}
```
Correct:
```java
@Entity @Table(name = "documents")
public class Document {
    @Column(name = "student_id", nullable = false)
    private Long studentId;                    // loose scalar FK, no cascade —
}                                              // mirrors the legacy SQLite schema
// upgrading to @ManyToOne is a deliberate, called-out change, not a drive-by
```

## Rule 9 — Schema changes are additive and non-destructive
Violation:
```java
// hand-run against the live shared DB:  ALTER TABLE students DROP COLUMN phone;
@Column(name = "phone", nullable = false)     // now NOT NULL with no default,
private String phone;                          // fails against existing rows
```
Correct:
```java
// add the field; ddl-auto=update ADDs the column and leaves existing data alone
@Column(name = "nickname")
private String nickname;                        // nullable / defaulted → safe on
                                                // a populated table. No DROP/RENAME.
```

## Rule 10 — Entity plumbing correct; identity stable
Violation:
```java
@Entity
public class Student {
    @Id private Long id;                        // no generation strategy
    public void setId(Long id) { this.id = id; }        // caller overwrites the PK
    @Override public boolean equals(Object o) { ... email ... }  // mutable-field identity
}
```
Correct:
```java
@Entity
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // matches SQLite AUTOINCREMENT
    private Long id;
    public Long getId() { return id; }          // no id setter
    public Student() {}                          // ORM-required no-arg constructor
    // equality (if defined) keys on id only, never on mutable business fields
}
```

## Rule 11 — Respect the datastore's concurrency limits
Violation:
```properties
# SQLite allows ONE writer; a bigger pool just produces SQLITE_BUSY under load
spring.datasource.hikari.maximum-pool-size=20
```
Correct:
```properties
spring.datasource.hikari.maximum-pool-size=1   # single writer, as SQLite requires
# code must not assume concurrent writers or hold long-open write transactions
```

## Rule 12 — Isolate persistence behind the repository seam
Violation:
```java
@Service
class StudentService {
    @PersistenceContext private EntityManager em;   // session mechanics in service
    List<Student> all() { return em.createQuery("from Student", Student.class).getResultList(); }
}
```
Correct:
```java
@Service
class StudentService {
    private final StudentRepository students;        // depends on the abstraction
    StudentService(StudentRepository students) { this.students = students; }
    List<Student> all() { return students.findAll(Sort.by("id")); }
}
```
