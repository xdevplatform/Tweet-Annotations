# [ ] TODO --> Add options for user (e.g. how many Tweets are returned to analyze; location for which to get Tweets, parameters to tune follower base - number of followers for sample & number of Tweets for each sampled follower, etc.)
# [ ] TODO --> Ensure if multiple users use this app it doesn't break (e.g. global variables)
# [ ] TODO --> Add visual charts: go more granular than the annotation domain. Make sure to return the annotation entity when displaying graphs.
# [ ] TODO --> Deploy

import os
from flask import (
    Flask,
    render_template,
    redirect,
    Response,
    send_from_directory,
    current_app,
)
from server.main import *
from forms import GetUsername, GetTopic, DropdownForm, GetKeyword

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY
SELECTED_DOMAIN_ID = None
CSV_PATH = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/GetTopicsForProfiles", methods=["post", "get"])
def get_topics_profile():
    global CSV_PATH
    top_emojis = 0
    form = GetUsername()
    response_code = None
    tweet_count = None
    annotations_data = None
    domain = None
    entity = None
    person = None
    place = None
    product = None
    organization = None
    other = None
    if form.validate_on_submit():
        username = form.username.data
        username, user_id = get_user_details(username)
        if user_id == None:
            annotations_data = 0
        else:
            user_timeline_tweets, response_code = get_user_tweet_timeline(user_id)
            if response_code != 200:
                annotations_data = 1
            else:
                (
                    tweet_count,
                    domain,
                    entity,
                    person,
                    place,
                    product,
                    organization,
                    other,
                ) = get_annotations(user_timeline_tweets)
                top_emojis_results = get_style(user_timeline_tweets, 4)
                top_emojis = " ".join(k for k, v in top_emojis_results.items())
                CSV_PATH = f"top_annotations_{username}.csv"
                export_to_csv(
                    CSV_PATH,
                    domain,
                    entity,
                    person,
                    place,
                    product,
                    organization,
                    other,
                )

    return render_template(
        "get_topics_for_profiles.html",
        form=form,
        annotations_data=annotations_data,
        top_emojis=top_emojis,
        tweet_count=tweet_count,
        domain=domain,
        entity=entity,
        person=person,
        place=place,
        product=product,
        organization=organization,
        other=other,
        response_code=response_code,
        methods=["post", "get"],
    )


@app.route("/GetTopicsForProfileFollowers", methods=["post", "get"])
def get_topics_follower_base():
    global CSV_PATH
    form = GetUsername()
    annotations_data = None
    response_code = None
    top_emojis = 0
    all_emojis = {}
    all_domain = {}
    all_entity = {}
    all_person = {}
    all_place = {}
    all_product = {}
    all_organization = {}
    all_other = {}
    tweet_count = 0
    follower_count = 0
    if form.validate_on_submit():
        username = form.username.data
        username, user_id = get_user_details(username)
        if user_id == None:
            annotations_data = 0
        else:
            user_followers, response_code = get_user_followers(user_id)
            follower_count = len(user_followers)
            if response_code != 200:
                annotations_data = 1
            else:
                follower_count = len(user_followers)
                follower_selection = random_selection(user_followers, follower_count)
                follower_selection_ids = [i["id"] for i in follower_selection]
                for follower_id in follower_selection_ids:
                    user_tweets, response_code = get_user_tweet_timeline_no_pagination(
                        follower_id
                    )
                    if response_code != 200:
                        annotations_data = 1
                    else:
                        (
                            count,
                            domain,
                            entity,
                            person,
                            place,
                            product,
                            organization,
                            other,
                        ) = get_annotations(user_tweets)
                        top_emojis_results = get_style(user_tweets, 0)
                        tweet_count += count
                        all_domain = update_annotations(all_domain, domain)
                        all_entity = update_annotations(all_entity, entity)
                        all_person = update_annotations(all_person, person)
                        all_place = update_annotations(all_place, place)
                        all_product = update_annotations(all_product, product)
                        all_organization = update_annotations(
                            all_organization, organization
                        )
                        all_other = update_annotations(all_other, other)
                        if top_emojis_results != 1:
                            all_emojis = update_annotations(
                                all_emojis, top_emojis_results
                            )

                    if len(all_emojis) != 0:
                        top_emojis_unsorted = {
                            k: v for (k, v) in all_emojis.items() if v > 2
                        }
                        top_emojis_sorted = {
                            k: v
                            for k, v in sorted(
                                top_emojis_unsorted.items(),
                                key=lambda item: item[1],
                                reverse=True,
                            )
                        }
                        top_emojis = " ".join(k for k, v in top_emojis_sorted.items())
                    elif len(all_emojis) == 0:
                        top_emojis = 1

                    # Sort annotations by order of frequency
                    all_domain_ordered = {
                        k: v
                        for k, v in sorted(
                            all_domain.items(), key=lambda item: item[1], reverse=True
                        )
                    }
                    all_entity_ordered = {
                        k: v
                        for k, v in sorted(
                            all_entity.items(), key=lambda item: item[1], reverse=True
                        )
                    }
                    all_person_ordered = {
                        k: v
                        for k, v in sorted(
                            all_person.items(), key=lambda item: item[1], reverse=True
                        )
                    }
                    all_place_ordered = {
                        k: v
                        for k, v in sorted(
                            all_place.items(), key=lambda item: item[1], reverse=True
                        )
                    }
                    all_product_ordered = {
                        k: v
                        for k, v in sorted(
                            all_product.items(), key=lambda item: item[1], reverse=True
                        )
                    }
                    all_organization_ordered = {
                        k: v
                        for k, v in sorted(
                            all_organization.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    }
                    all_other_ordered = {
                        k: v
                        for k, v in sorted(
                            all_other.items(), key=lambda item: item[1], reverse=True
                        )
                    }

                    # Only return annotations that are present in at least 2 Tweets
                    all_domain = {k: v for k, v in all_domain_ordered.items() if v >= 2}
                    all_entity = {k: v for k, v in all_entity_ordered.items() if v >= 2}
                    all_person = {k: v for k, v in all_person_ordered.items() if v >= 2}
                    all_place = {k: v for k, v in all_place_ordered.items() if v >= 2}
                    all_product = {
                        k: v for k, v in all_product_ordered.items() if v >= 2
                    }
                    all_organization = {
                        k: v for k, v in all_organization_ordered.items() if v >= 2
                    }
                    all_other = {k: v for k, v in all_other_ordered.items() if v >= 2}

                    CSV_PATH = f"top_annotations_{username}_followers.csv"

                    export_to_csv(
                        CSV_PATH,
                        all_domain,
                        all_entity,
                        all_person,
                        all_place,
                        all_product,
                        all_organization,
                        all_other,
                    )

    return render_template(
        "get_topics_for_profile_followers.html",
        form=form,
        follower_count=follower_count,
        annotations_data=annotations_data,
        tweet_count=tweet_count,
        top_emojis=top_emojis,
        domain=all_domain,
        entity=all_entity,
        person=all_person,
        place=all_place,
        product=all_product,
        organization=all_organization,
        other=all_other,
        response_code=response_code,
        methods=["post", "get"],
    )


@app.route("/DownloadCSV", methods=["post", "get"])
def download_csv():
    global CSV_PATH
    uploads = current_app.root_path + "/" + CSV_PATH
    csv = open(uploads, "r")
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={uploads}"},
    )


@app.route("/GetProfilesForTopic", methods=["post", "get"])
def get_profiles():
    global SELECTED_DOMAIN_ID

    users = []

    query = """SELECT * FROM domains
            ORDER by 2;
            """
    domains = get_data_from_db(query)

    if SELECTED_DOMAIN_ID is not None:
        query = f"""SELECT entity_id, entity_name FROM entities
                WHERE domain_id = {SELECTED_DOMAIN_ID} 
                ORDER BY 2;
                """
        entities = get_data_from_db(query)
    else:
        entities = [(-1, "None")]

    domains_form = construct_dropdown(domains)
    entities_form = construct_dropdown(entities)

    if domains_form.validate_on_submit():
        domain_id = domains_form.data["select"]
        SELECTED_DOMAIN_ID = domain_id

        query = f"""SELECT entity_id, entity_name FROM entities
                WHERE domain_id = {SELECTED_DOMAIN_ID} 
                ORDER BY 2;
                """
        entities = get_data_from_db(query)
        entities_form = construct_dropdown(entities)

    if entities_form.validate_on_submit():
        entity_id = entities_form.data["select"]

        topic = SELECTED_DOMAIN_ID + "." + entity_id

        query = f"context:{topic} is:verified -is:nullcast lang:en"
        tweets = search_tweets(query)
        if tweets == None:
            users = 0
        elif "data" not in tweets[0]:
            users = 1
        else:
            users = get_users(tweets)

    return render_template(
        "get_profiles_for_topic.html",
        domains_form=domains_form,
        entities_form=entities_form,
        users=users,
        methods=["post", "get"],
    )


@app.route("/GetTweetMetricsForTopic", methods=["post", "get"])
def get_metrics():
    form = GetKeyword()
    keyword = None
    status_code = None
    tweet_ids = []
    tweet_count = 0
    retweet_count = 0
    like_count = 0
    reply_count = 0
    quote_count = 0
    if form.validate_on_submit():
        keyword = form.keyword.data
        query = f"{keyword} place_country:GB -is:retweet -is:reply -is:nullcast lang:en"
        tweets, status_code = search_tweets_with_pagination(query)

        tweet_count = len(tweets)

        if status_code != 200:
            keyword = 1
        else:
            if tweets == None:
                keyword = 1
            elif tweet_count < 1:
                keyword = 0
            else:
                for i, tweet in enumerate(tweets):
                    if i > 5:
                        break
                    if tweet["id"]:
                        tweet_ids.append(tweet["id"])

        retweet_count, like_count, reply_count, quote_count = get_tweet_metrics(tweets)

    return render_template(
        "get_tweet_metrics_for_topic.html",
        form=form,
        tweet_ids=tweet_ids,
        status_code=status_code,
        tweet_count=tweet_count,
        keyword=keyword,
        retweet_count=retweet_count,
        like_count=like_count,
        reply_count=reply_count,
        quote_count=quote_count,
        methods=["post", "get"],
    )
