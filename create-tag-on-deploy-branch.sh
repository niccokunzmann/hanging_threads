#!/bin/bash
#
# When we are on a branch of the form vNUNMBER.NUMBER,
# for each commit, we replace the __version__ information
# in the hanging_threads.py with a running number of tags,
# i.E. branch v2.1 leads to the tags v2.1.0, v2.1.1, ... .
#
set -e

echo "(1) check if we are on a deploy branch of the form vNUMBER.NUMBER"

# get current branch name
# http://stackoverflow.com/a/1418022/367456
if [ "$TRAVIS_PULL_REQUEST" == "false" ] || [ -z "$TRAVIS_PULL_REQUEST" ]
then
  echo "This is not a pull request."
  if [ -z "$TRAVIS_BRANCH" ]
  then
    echo "This seems to be executed locally and not on travis. Getting current branch."
    current_branch="`git rev-parse --abbrev-ref HEAD`"
  else
    echo "We are on travis and can use the environment variables to know the branch."
    current_branch="$TRAVIS_BRANCH"
  fi
else
  echo "This is a pull request. We can not build from a pull request."
  exit 0
fi

if echo "$current_branch" | grep -qE '^v[[:digit:]]+\.[[:digit:]]+$'
then
  echo "Branch $current_branch is a deploy branch."
else
  echo "Branch $current_branch is not a deploy branch."
  exit 0
fi

echo "(2) Check if we are not on a tag to prevent build loops."
# http://stackoverflow.com/a/27911598/1320237
git fetch --tags
tags_to_head="`git tag --points-at HEAD`"
if [ -n "$tags_to_head" ]
then
  echo "The tag" $tags_to_head "points to this commit. It cannot be used to create a new tag."
  exit 0
else
  echo "This commit has no tags pointing at it. It can be used for a build."
fi

echo "(3) compute increasing tag number"

tags="`git tag -l \"${current_branch}.*\"`"
echo "Previous tags:" $tags
i=0
function new_tag() {
  echo -n "$current_branch.$i"
}
while echo "$tags" | grep -qx "`new_tag`"
do
  # arithmetic http://stackoverflow.com/a/6348941/1320237
  i=$((i + 1))
done
echo "The new tag is `new_tag`"

echo "(4) change version of hanging_threads.py"
file="hanging_threads.py"
sed -ri "0,/__version__\\s*=\\s*(\"[^\"]*\"|'[^']*')/ s//__version__ = \"`new_tag`\"/" "$file"
cat "$file" | grep -F "__version__"

echo "(5) Create git tag `new_tag`"
git add "$file"
git config user.email || git config user.email "travis@travis-ci.org"
git config user.name || git config user.name "Travis CI"
git commit -m"automatic commit by `whoami`@`hostname` for tag `new_tag` $TRAVIS_BUILD_NUMBER"
git tag "`new_tag`"

echo "(6) pushing back to travis"
push_url="$1"
if [ -z "$push_url" ]
then
  echo "No push url found as first argument. Will not push the tag `new_tag`."
  exit 0
else
  echo "Push url found as first argument! Trying to push."
fi

# Using ideas from https://gist.github.com/willprice/e07efd73fb7f13f917ea
# piping away the output because it could contain the url
if git push --quiet "$push_url" "`new_tag`" 1>>/dev/null 2>>/dev/null
then
  echo "Push successful."
else
  echo "Push failed."
  exit 1
fi
