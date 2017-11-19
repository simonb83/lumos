--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.3
-- Dumped by pg_dump version 9.5.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: gofundme; Type: TABLE; Schema: public; Owner: lumos
--

CREATE TABLE gofundme (
    id integer NOT NULL,
    url text,
    page_num integer,
    date_added timestamp without time zone DEFAULT now(),
    country_term text,
    country character varying(15)
);


ALTER TABLE gofundme OWNER TO lumos;

--
-- Name: gofundme_id_seq; Type: SEQUENCE; Schema: public; Owner: lumos
--

CREATE SEQUENCE gofundme_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE gofundme_id_seq OWNER TO lumos;

--
-- Name: gofundme_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: lumos
--

ALTER SEQUENCE gofundme_id_seq OWNED BY gofundme.id;


--
-- Name: rawdata; Type: TABLE; Schema: public; Owner: lumos
--

CREATE TABLE rawdata (
    url_id integer NOT NULL,
    goal character varying(15),
    raised character varying(20),
    raised_by character varying(10),
    date_created character varying(40),
    loc_name character varying(40),
    content character varying,
    currency character varying(3),
    goal_num integer,
    raised_num integer,
    campaign_date date,
    loc_code character varying(8),
    relevant boolean,
    campiagn_size character varying(1)
);


ALTER TABLE rawdata OWNER TO lumos;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: lumos
--

ALTER TABLE ONLY gofundme ALTER COLUMN id SET DEFAULT nextval('gofundme_id_seq'::regclass);


--
-- Name: gofundme_pkey; Type: CONSTRAINT; Schema: public; Owner: lumos
--

ALTER TABLE ONLY gofundme
    ADD CONSTRAINT gofundme_pkey PRIMARY KEY (id);


--
-- Name: rawdata_pkey; Type: CONSTRAINT; Schema: public; Owner: lumos
--

ALTER TABLE ONLY rawdata
    ADD CONSTRAINT rawdata_pkey PRIMARY KEY (url_id);


--
-- Name: unique_url; Type: CONSTRAINT; Schema: public; Owner: lumos
--

ALTER TABLE ONLY gofundme
    ADD CONSTRAINT unique_url UNIQUE (url);


--
-- Name: public; Type: ACL; Schema: -; Owner: lumos
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM lumos;
GRANT ALL ON SCHEMA public TO lumos;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

