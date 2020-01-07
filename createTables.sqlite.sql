CREATE TABLE "printers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(42)   NOT NULL,
    "deprecation" REAL   NOT NULL,
    "default_electric_consumption" REAL   NOT NULL
);

CREATE TABLE "filaments" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(42)   NOT NULL,
    "color" VARCHAR(15),
    "total_cost" REAL   NOT NULL,
    "length" INTEGER   NOT NULL,
    "material_name" VARCHAR(10)   NOT NULL,
    FOREIGN KEY(material_name) REFERENCES materials(name)
);

CREATE TABLE "materials" (
    "name" VARCHAR(10)   PRIMARY KEY
);

CREATE TABLE "materials_consumptions" (
    "consumption" REAL   NOT NULL,
    "material_name" VARCHAR(10) NOT NULL,
    "printer_id" INTEGER NOT NULL,
    UNIQUE (material_name,printer_id),
    FOREIGN KEY(printer_id) REFERENCES printers(id),
    FOREIGN KEY(material_name) REFERENCES materials(name)
);

CREATE TABLE "orders" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "description" TEXT,
    "net_cost" REAL   NOT NULL,
    "customer_cost" REAL   NOT NULL,
    "customer_id" INTEGER NOT NULL,
    "unix_time" INTEGER   NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE "customers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" VARCHAR(42)   NOT NULL,
    "last_name" VARCHAR(42),
    "phone_number" INTEGER
);

CREATE TABLE "filament_order" (
    "filament_id" INTEGER   NOT NULL,
    "order_id" INTEGER NOT NULL,
    "length" INTEGER NOT NULL,
    "printing_time" INTEGER NOT NULL,
    "printer_id" INTEGER NOT NULL,
    UNIQUE (filament_id,order_id),
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(filament_id) REFERENCES filaments(id),
    FOREIGN KEY(printer_id) REFERENCES printers(id)
);

CREATE TABLE "human_time" (
    "order_id" INTEGER NOT NULL,
    "support_removal" INTEGER NOT NULL,
    "slicing" INTEGER NOT NULL,
    "print_removal" INTEGER NOT NULL,
    "set_up_printer" INTEGER NOT NULL,
    UNIQUE (order_id),
    FOREIGN KEY(order_id) REFERENCES orders(id)
);

INSERT INTO printers (name, deprecation, default_electric_consumption) VALUES ("human",200, 0);
INSERT INTO materials (name) VALUES ("pla");
INSERT INTO materials (name) VALUES ("petg");
INSERT INTO materials (name) VALUES ("abs");
INSERT INTO materials (name) VALUES ("tpu");
INSERT INTO customers (name) VALUES ("GENERIC");
COMMIT
