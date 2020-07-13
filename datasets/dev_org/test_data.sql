BEGIN TRANSACTION;
CREATE TABLE "Account" (
	id INTEGER NOT NULL,
	"Name" VARCHAR(255),
	"BillingCountry" VARCHAR(255),
	"BillingStreet" VARCHAR(255),
	"BillingState" VARCHAR(255),
	"BillingCity" VARCHAR(255),
	"BillingPostalCode" VARCHAR(255),
  "ShippingCountry" VARCHAR(255),
	"ShippingStreet" VARCHAR(255),
	"ShippingState" VARCHAR(255),
	"ShippingCity" VARCHAR(255),
	"ShippingPostalCode" VARCHAR(255),
	"npe01__SYSTEM_AccountType__c" VARCHAR(255),
  "npo02__HouseholdPhone__c" VARCHAR(255)
	PRIMARY KEY (id)
);
INSERT INTO "Account" VALUES(1,'Patterson Household','Argentina','26 Blackbird Junction','','La Banda','','Household Account');
COMMIT;