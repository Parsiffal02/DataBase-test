/*----------------------Ratings-------------------*/

create or replace function add_rating(in business_name text, in feedback text, in grade integer)
	returns void
	language sql
	as $$

	insert into "Ratings" (business_name, feedback, grade)
    values (business_name, feedback, grade)

$$;

create or replace function delete_rating(in business_name0 text)
	returns void
	language sql
	as $$

	delete from "Ratings" where business_name = business_name0

$$;

create or replace function get_ratings()
	returns json
	language plpgsql
	as $$
		begin
		   return (select json_agg(json_build_object(
				'business_name', "Ratings".business_name,
				'feedback', "Ratings".feedback,
				'grade', "Ratings".grade)) from "Ratings");
		end
$$;

create or replace function delete_ratings()
	returns void
	language sql
	as $$

	truncate "Ratings"

$$;

create or replace function search_ratings(in business_name0 text)
	returns json
	language plpgsql
	as $$
		begin
		   return (select json_agg(json_build_object(
		        'business_name', "Ratings".business_name,
				'feedback', "Ratings".feedback,
				'grade', "Ratings".grade)) from "Ratings" where business_name = business_name0);
		end
	$$;

/*------------------------------------------------*/


/*------------------------------Suppliers--------------------------*/

create or replace function add_supplier(in organisation text, in reviews text, in phone_number varchar(11))
	returns void
	language sql
	as $$

	insert into "Suppliers" (organisation,reviews,phone_number)
    values (organisation, reviews, phone_number)

$$;

create or replace function delete_supplier(in organisation0 text)
	returns void
	language sql
	as $$

	delete from "Suppliers" where organisation = organisation0

$$;

create or replace function get_suppliers()
	returns json
	language plpgsql
	as $$
		begin
		   return (select json_agg(json_build_object(
				'organisation', "Suppliers".organisation,
				'reviews', "Suppliers".reviews ,
				'phone_number', "Suppliers".phone_number)) from "Suppliers");
		end
	$$;

create or replace function delete_suppliers()
	returns void
	language sql
	as $$

	truncate "Suppliers"

$$;

create or replace function search_supplier(in phone_number0 varchar(11))
	returns json
	language plpgsql
	as $$
		begin
		   return (select json_agg(json_build_object(
				'organisation', "Suppliers".organisation,
				'reviews', "Suppliers".reviews ,
				'phone_number', "Suppliers".phone_number)) from "Suppliers" where phone_number = phone_number0);
		end
	$$;

create or replace function update_supplier(in new_organisation text, in organisation0 text)
	returns void
	language sql
	as $$

	update "Suppliers" set organisation = new_organisation where organisation = organisation0

$$;

/*------------------------------Owners-----------------------------*/

create or replace function add_owner(in name1 text, in foundation_date date, in email text)
	returns void
	language sql
	as $$

	insert into "Owners" (name, foundation_date, email)
    values (name1, foundation_date, email)

$$;

create or replace function delete_owner(in name0 text)
	returns void
	language sql
	as $$

	delete from "Owners" where name = name0

$$;

create or replace function get_owners()
	returns json
	language plpgsql
	as $$
		begin
		   return (select json_agg(json_build_object(
				'name', "Owners".name,
				'foundation_date', "Owners".foundation_date,
				'email', "Owners".email)) from "Owners");
		end
	$$;

create or replace function delete_owners()
	returns void
	language sql
	as $$

	truncate "Owners"

$$;

create or replace function search_owner(in email0 text)
	returns json
	language plpgsql
	as $$
		begin
		   return (select json_agg(json_build_object(
				'name', "Owners".name,
				'foundation_date', "Owners".foundation_date,
				'email', "Owners".email)) from "Owners" where email = email0);
		end
	$$;

create or replace function update_owner(in new_name text, in name0 text)
	returns void
	language sql
	as $$

	update "Owners" set name = new_name where name = name0

$$;

/*--------------------------------------------------------------------*/

/*--------------------------------Business--------------------------*/

create or replace function add_business(in name text, in address text, in supplier text, in owner text, in feature text)
	returns void
	language sql
	as $$

	insert into "Business"(name,address,supplier,owner,feature)
    values (name, address, supplier, owner, feature)

$$;

create or replace function delete_business(in name0 text)
	returns void
	language sql
	as $$

	delete from "Business" where name = name0

$$;

create or replace function get_business()
	returns json
	language plpgsql
	as $$
		begin
		   return (select json_agg(json_build_object(
		        'id', "Business".id,
		        'name', "Business".name,
				'address', "Business".address,
				'supplier', "Business".supplier,
				'owner', "Business".owner,
				'feature', "Business".feature)) from "Business");
		end
	$$;

create or replace function delete_businesses()
	returns void
	language sql
	as $$

	truncate "Business"

$$;

create or replace function search_business(in name0 text)
	returns json
	language plpgsql
	as $$
		begin
		   return (select json_agg(json_build_object(
		        'id', "Business".id,
		        'name', "Business".name,
				'address', "Business".address,
				'supplier', "Business".supplier,
				'owner', "Business".owner,
				'feature', "Business".feature)) from "Business" where name = name0);
		end
	$$;

create or replace function update_business(in new_name text, in name0 text)
	returns void
	language sql
	as $$

	update "Business" set name = new_name where name = name0

$$;

/*--------------------------------------------------------------------------*/