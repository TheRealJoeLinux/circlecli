# -*- coding: utf-8 -*-
"""CLI wrapper for CircleCI's REST API."""
import requests
from urllib import urlencode
from urlparse import ParseResult, urlparse, urlunparse


class CircleAPI(object):
    """Simple wrapper for requests specific to CircleCI."""

    def __init__(self, token):
        """Load the API token.

        Args:
            token (str): the CircleCI API token (obtained at https://circleci.com/account/api)
        """
        self._token = token
        self._base_url = "https://circleci.com/api/v1"

    def _build_url(self, endpoint, params={}):
        """Return the full URL for the desired endpoint.

        Args:
            endpoint (str): the API endpoint after base URL
            params (dict): any params to include in the request

        Returns:
            (str) the full URL of the request
        """
        new_params = {'circle-token': self._token}
        new_params.update(params)

        parsed_url = urlparse(self._base_url)
        new_parse = ParseResult(scheme=parsed_url.scheme, netloc=parsed_url.netloc,
                                path='/'.join((parsed_url.path, endpoint)),
                                params='', query=urlencode(new_params),
                                fragment='')

        return urlunparse(new_parse)

    def _get(self, endpoint, params={}, headers={}):
        """Send a GET request to `endpoint`.

        Args:
            endpoint (str): the API endpoint after base URL
            params (dict): any params to include in the request
            headers (dict): any headers to include in the request

        Returns:
            (dict) the JSON-converted response from the endpoint
        """
        url = self._build_url(endpoint, params)
        new_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        new_headers.update(headers)

        r = requests.get(url, headers=new_headers)
        if r.status_code >= 400:
            raise Exception(u"Error sending GET request to {}".format(url))

        return r.json()

    def _post(self, endpoint, data=None, headers={}):
        """Send a POST request to `endpoint`.

        Args:
            endpoint (str): the API endpoint after base URL
            data (dict): the body to submit with the request
            headers (dict): any headers to include in the request

        Returns:
            (dict) the JSON-converted response from the endpoint
        """
        url = self._build_url(endpoint)
        new_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        new_headers.update(headers)

        r = requests.post(url, headers=new_headers, data=data)
        if r.status_code >= 400:
            raise Exception(u"Error sending POST request to {}".format(url))

        return r.json()

    def _delete(self, endpoint, headers={}):
        """Send a DELETE request to `endpoint`.

        Args:
            endpoint (str): the API endpoint after base URL
            headers (dict): any headers to include in the request

        Returns:
            (dict) the JSON-converted response from the endpoint
        """
        url = self._build_url(endpoint)
        new_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        new_headers.update(headers)

        r = requests.delete(url, headers=headers)
        if r.status_code >= 400:
            raise Exception(u"Error sending DELETE request to {}".format(url))

        return r.json()

    def me(self):
        """Provide information about the signed in user.

        Returns:
            (dict) the JSON-converted response from the endpoint
        """
        return self._get('me')

    def projects(self):
        """List of all the projects you're following on CircleCI.

        Returns:
            (list) a list of all the projects and project info
        """
        return self._get('projects')

    def project_builds(self, username, project):
        """Build summary for each of the last 30 builds for a single git repo.

        Args:
            username (str): the owner of the project
            project (str): the project name

        Returns:
            (list) a list of builds for the project
        """
        return self._get('project/{username}/{project}'.format(locals()))

    def recent_builds(self):
        """Build summary for each of the last 30 recent builds.

        Returns:
            (list) a list of builds
        """
        return self._get('recent-builds')

    def build_details(self, username, project, build_num):
        """Full details for a single build.

        Args:
            username (str): the owner of the project
            project (str): the project name
            build_num (int): the build number

        The response includes all of the fields from the build summary. This is
        also the payload for the [notification webhooks](https://circleci.com/docs/configuration/#notify),
        in which case this object is the value to a key named 'payload'.

        Returns:
            (dict) the full details for the build
        """
        return self._get('project/{username}/{project}/{build_num}'.format(locals()))

    def artifacts(self, username, project, build_num):
        """List the artifacts produced by a given build.

        Args:
            username (str): the owner of the project
            project (str): the project name
            build_num (int): the build number

        Returns:
            (list) the artifacts produced by the build
        """
        return self._get('project/{username}/{project}/{build_num}/artifacts'.format(locals()))

    def retry_build(self, username, project, build_num):
        """Retry a given build.

        Args:
            username (str): the owner of the project
            project (str): the project name
            build_num (int): the build number

        Returns:
            (dict) a summary of the new build
        """
        return self._post('project/{username}/{project}/{build_num}/retry'.format(locals()))

    def cancel_build(self, username, project, build_num):
        """Cancel a given build.

        Args:
            username (str): the owner of the project
            project (str): the project name
            build_num (int): the build number

        Returns:
            (dict) a summary of the canceled build
        """
        return self._post('project/{username}/{project}/{build_num}/cancel'.format(locals()))

    def ssh_users(self, username, project, build_num):
        """Add a user to the build's SSH permissions.

        Args:
            username (str): the owner of the project
            project (str): the project name
            build_num (int): the build number

        Returns:
            (dict) confirmation of the added user
        """
        raise NotImplementedError(u"This method has not yet been implemented.")

    def new_build(self, username, project, branch):
        """Trigger a new build.

        Args:
            username (str): the owner of the project
            project (str): the project name
            branch (str): the branch to use for the build

        Returns:
            (dict) a summary of the new build
        """
        raise NotImplementedError(u"This method has not yet been implemented.")

    def create_ssh(self, username, project):
        """Create an SSH key used to access key-based external systems.

        Args:
            username (str): the owner of the project
            project (str): the project name

        Returns:
            (dict) confirmation of the added key
        """
        raise NotImplementedError(u"This method has not yet been implemented.")

    def list_checkout_keys(self, username, project):
        """List checkout keys.

        Args:
            username (str): the owner of the project
            project (str): the project name

        Returns:
            (list) the checkout keys
        """
        return self._get('project/{username}/{project}/checkout-key'.format(locals()))

    def create_checkout_key(self, username, project):
        """List checkout keys.

        Args:
            username (str): the owner of the project
            project (str): the project name

        Returns:
            (dict) confirmation of the added key
        """
        raise NotImplementedError(u"This method has not yet been implemented.")

    def checkout_key(self, username, project, fingerprint):
        """Get a checkout key.

        Args:
            username (str): the owner of the project
            project (str): the project name
            fingerprint (str): the fingerprint of the checkout key

        Returns:
            (dict) a single checkout key
        """
        return self._get('project/{username}/{project}/checkout-key/{fingerprint}'.format(locals()))

    def delete_checkout_key(self, username, project, fingerprint):
        """Delete a checkout key.

        Args:
            username (str): the owner of the project
            project (str): the project name
            fingerprint (str): the fingerprint of the checkout key

        Returns:
            (dict) a single checkout key
        """
        return self._delete('project/{username}/{project}/checkout-key/{fingerprint}'.format(locals()))

    def clear_cache(self, username, project):
        """Clear the cache for a project.

        Args:
            username (str): the owner of the project
            project (str): the project name

        Returns:
            (dict) confirmation of the cleared cache
        """
        return self._delete('project/{username}/{project}/build-cache'.format(locals()))

    def add_circle_key(self):
        """Add a CircleCI key to your GitHub user account.

        Returns:
            (dict) confirmation of the key addition
        """
        raise NotImplementedError(u"This method has not yet been implemented.")

    def add_heroku_key(self):
        """Add your Heroku API key to CircleCI.

        Returns:
            (dict) confirmation of the key addition
        """
        raise NotImplementedError(u"This method has not yet been implemented.")