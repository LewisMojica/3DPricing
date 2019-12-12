CREATE TABLE "printers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(42)   NOT NULL,
    "depracation" INTEGER   NOT NULL
);

CREATE TABLE "filaments" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(42)   NOT NULL,
    "total_cost" INTEGER   NOT NULL,
    "length" INTEGER   NOT NULL,
    "actual_length" INTEGER,
    "material_name" VARCHAR(10)   NOT NULL,
    FOREIGN KEY(material_name) REFERENCES materials(name)
);

CREATE TABLE "materials" (
    "name" VARCHAR(10)   PRIMARY KEY
);

CREATE TABLE "materials_consumptions" (
    "consumption" INTEGER   NOT NULL,
    "material_name" VARCHAR(10) NOT NULL,
    "printer_id" INTEGER NOT NULL,
    UNIQUE (material_name,printer_id),
    FOREIGN KEY(printer_id) REFERENCES printers(id),
    FOREIGN KEY(material_name) REFERENCES materials(name)
);

CREATE TABLE "orders" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "description" TEXT,
    "net_cost" INTEGER   NOT NULL,
    "customer_cost" INTEGER   NOT NULL,
    "customer_id" INTEGER NOT NULL,
    "printer_id" INTEGER NOT NULL,
    "year" INTEGER   NOT NULL,
    "month" INTEGER   NOT NULL,
    "day" INTEGER   NOT NULL,
    "hour" INTEGER   NOT NULL,
    "second" INTEGER   NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(printer_id) REFERENCES printers(id)
);

CREATE TABLE "customers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(42)   NOT NULL,
    "last_name" VARCHAR(42),
    "phone_number" INTEGER
);

CREATE TABLE "filaments_orders" (
    "filament_id" INTEGER   NOT NULL,
    "order_id" INTEGER NOT NULL,
    "length" INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(filament_id) REFERENCES filaments(id)
)